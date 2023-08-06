#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Michael J. Hayford
""" First order paraxial design space

.. Created on Sat Mar 31 21:14:42 2018

.. codeauthor: Michael J. Hayford
"""

import numpy as np

from rayoptics.optical.model_constants import ht, slp, aoi
from rayoptics.optical.model_constants import pwr, tau, indx, rmd
import rayoptics.optical.model_constants as mc
import rayoptics.parax.firstorder as fo
from rayoptics.seq.gap import Gap
from rayoptics.elem.surface import Surface

from rayoptics.util.line_intersection import get_intersect
from numpy.linalg import norm


def bbox_from_poly(poly):
    minx, miny = np.min(poly, axis=0)
    maxx, maxy = np.max(poly, axis=0)
    return np.array([[minx, miny], [maxx, maxy]])


class ParaxialModel():
    def __init__(self, opt_model, opt_inv=1.0, ifcs_mapping=None, **kwargs):
        self.opt_model = opt_model
        self.seq_model = opt_model.seq_model
        self.ifcs_mapping = ifcs_mapping
        self.sys = []
        self.ax = []
        self.pr = []
        self.opt_inv = opt_inv

    def __json_encode__(self):
        attrs = dict(vars(self))
        del attrs['opt_model']
        del attrs['seq_model']
        del attrs['parax_data']
        return attrs

    def sync_to_restore(self, opt_model):
        self.opt_model = opt_model
        self.seq_model = opt_model.seq_model
        if not hasattr(self, 'ifcs_mapping'):
            self.ifcs_mapping = None

    def update_model(self):
        self.parax_data = self.opt_model.optical_spec.parax_data
        self.build_lens()

    def build_lens(self):
        # rebuild the `sys` description from the seq_model path
        self.sys = sys = self.seq_path_to_paraxial_lens(self.seq_model.path())

        # precalculate the reduced forms of the paraxial axial and chief rays
        if self.parax_data is not None:
            ax_ray, pr_ray, fod = self.parax_data
            self.opt_inv = fod.opt_inv
    
            self.ax = []
            self.pr = []
            for i in range(0, len(sys)):
                n = sys[i][indx]
                self.ax.append([ax_ray[i][ht], n*ax_ray[i][slp], n*ax_ray[i][aoi]])
                self.pr.append([pr_ray[i][ht], n*pr_ray[i][slp], n*pr_ray[i][aoi]])

    def get_pt(self, idx):
        return self.pr[idx][mc.ht], self.ax[idx][mc.ht]

    def set_pt(self, idx, pt):
        self.pr[idx][mc.ht] = pt[0]
        self.ax[idx][mc.ht] = pt[1]

    def get_gap_for_node(self, node):
        if self.ifcs_mapping is None:
            # just return the node in the seq_model
            gap_idx = node
        else:  # use the air_gap_list to map to the seq_model
            air_gap_list, node_defs, map_to_ifcs = self.ifcs_mapping
            kernel = node_defs[node]
            if len(kernel) == 1:
                gap_idx = kernel[0]
            elif len(kernel) == 2:
                prev_gap_idx, following_gap_idx = kernel
                gap_idx = prev_gap_idx
        return self.seq_model.gaps[gap_idx], self.seq_model.z_dir[gap_idx]

    # --- add/delete points from diagram
    def add_node(self, node, new_vertex, type_sel, interact_mode):
        """ Add a node in the paraxial data structures """
        ns = self.seq_model.get_num_surfaces()
        if node >= ns - 1:
            node = ns - 2
        n = self.sys[node][indx]
        new_node = node + 1
        self.sys.insert(new_node, [0.0, 0.0, n, interact_mode])

        ax_node = [0.0, 0.0, 0.0]
        ax_node[type_sel] = new_vertex[1]
        self.ax.insert(new_node, ax_node)

        pr_node = [0.0, 0.0, 0.0]
        pr_node[type_sel] = new_vertex[0]
        self.pr.insert(new_node, pr_node)

        if type_sel == ht:
            self.apply_ht_dgm_data(new_node, new_vertex=new_vertex)
        elif type_sel == slp:
            self.apply_slope_dgm_data(new_node, new_vertex=new_vertex)

        if interact_mode == 'reflect':
            for i in range(new_node, len(self.sys)):
                self.sys[i][indx] = -self.sys[i][indx]

        return new_node

    def assign_object_to_node(self, node, factory, **inputs):
        """ create a new element from `factory` and replace `node` with it """

        # extract optical properties of node
        n = self.sys[node][indx]
        power = self.sys[node][pwr]
        thi = n*self.sys[node][tau]
        sd = abs(self.ax[node][ht]) + abs(self.pr[node][ht])

        # create an element with the node's properties
        seq, ele, e_node = descriptor = factory(power=power, sd=sd)

        n_before = self.sys[node-1][indx]
        thi_before = n_before*self.sys[node-1][tau]
        self.seq_model.gaps[node-1].thi = thi_before

        # insert the path sequence and elements into the
        #  sequential and element models
        kwargs = {'idx': node-1, 't': thi, **inputs}
        self.opt_model.insert_ifc_gp_ele(*descriptor, **kwargs)

        path_stop = node + len(seq)
        inserted_seq = list(self.seq_model.path(start=node-1, stop=path_stop))
        sys_seq = self.seq_path_to_paraxial_lens(inserted_seq[1:])
        pp_info = self.compute_principle_points(inserted_seq)
        self.replace_node_with_seq(node, sys_seq, pp_info)
        self.compute_signed_rindx()

        return descriptor, kwargs

    def compute_signed_rindx(self):
        """Reset the state of the refractive index array.
        
        This method resets the signs of the refractive indices so that they are
        negative following an odd number of reflections, but positive otherwise.
        """
        flip = 1
        for ss in self.sys:
            ss[indx] = abs(ss[indx])
            if ss[rmd] == 'reflect':
                flip = -flip
            if flip < 0:
                ss[indx] = -ss[indx]

    def replace_node_with_seq(self, node, sys_seq, pp_info):
        """ replaces the data at node with sys_seq """
        sys = self.sys
        ax = self.ax
        pr = self.pr
        if len(sys_seq) == 1:
            sys[node] = sys_seq[0]
        else:
            opt_inv = self.opt_inv
            efl, pp1, ppk, ffl, bfl = pp_info[2]
            sys[node-1][tau] -= pp1/sys[node-1][indx]
    
            # sys_seq[-1][tau] = sys[node][tau] - ppk/sys_seq[-1][indx]
            p0 = [ax[node][ht], pr[node][ht]]
            pn = [ax[node+1][ht], pr[node+1][ht]]
            slp0 = [ax[node][slp], pr[node][slp]]
    
            for n, ss in enumerate(sys_seq[:-1], start=node):
                sys.insert(n, ss)
    
                ax_ht = ax[n-1][ht] + sys[n-1][tau]*ax[n-1][slp]
                ax_slp = ax[n-1][slp] - ax_ht*sys[n][pwr]
                ax.insert(n, [ax_ht, ax_slp, 0.0])
    
                pr_ht = pr[n-1][ht] + sys[n-1][tau]*pr[n-1][slp]
                pr_slp = pr[n-1][slp] - pr_ht*sys[n][pwr]
                pr.insert(n, [pr_ht, pr_slp, 0.0])
    
            # replace the original node data
            ax[n+1][slp] = slp0[0]
            pr[n+1][slp] = slp0[1]
            sys[n+1][pwr] = (ax[n][slp]*pr[n+1][slp] -
                             ax[n+1][slp]*pr[n][slp])/opt_inv
            # sys_seq[-1][pwr]
            p1 = [ax[n][ht], pr[n][ht]]
            p2 = [ax[n][ht]+ax[n][slp], pr[n][ht]+pr[n][slp]]
            p2int = np.array(get_intersect(p1, p2, p0, pn))
            ax[n+1][ht] = p2int[0]
            pr[n+1][ht] = p2int[1]
            sys[n][tau] = (
                (ax[n][ht]*pr[n+1][ht] - ax[n+1][ht]*pr[n][ht])/opt_inv)
            sys[n+1][tau] = (p2int[0]*pn[1] - pn[0]*p2int[1])/opt_inv

    def get_object_for_node(self, node):
        ''' basic 1:1 relationship between seq and parax model sequences '''
        ifc = self.seq_model.ifcs[node]
        e_node = self.opt_model.part_tree.parent_node(ifc)
        args = [[ifc, None, None, 1, 1]], [e_node.id], e_node
        kwargs = {'idx': node}
        return args, kwargs

    def delete_node(self, surf):
        """ delete the node at position surf """
        del self.sys[surf]
        del self.ax[surf]
        del self.pr[surf]

    # --- edit diagram points
    def apply_ht_dgm_data(self, surf, new_vertex=None):
        """ This routine calculates all data dependent on the input
            height coordinates (y,ybar) at surface surf.
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr
        opt_inv = self.opt_inv

        if new_vertex is not None:
            pr_ray[surf][ht] = new_vertex[0]
            ax_ray[surf][ht] = new_vertex[1]

        nsm1 = len(sys) - 1
        if surf == 0:
            surf += 1

        p = surf - 1
        c = surf

        sys[p][tau] = ((ax_ray[p][ht]*pr_ray[c][ht] -
                        ax_ray[c][ht]*pr_ray[p][ht]) / opt_inv)
        ax_ray[p][slp] = (ax_ray[c][ht] - ax_ray[p][ht])/sys[p][tau]
        pr_ray[p][slp] = (pr_ray[c][ht] - pr_ray[p][ht])/sys[p][tau]

        if (surf > 1):
            p2 = surf - 2
            sys[p][pwr] = ((ax_ray[p2][slp]*pr_ray[p][slp] -
                            ax_ray[p][slp]*pr_ray[p2][slp])
                           / opt_inv)

        if (surf < nsm1):
            s = surf + 1

            sys[c][tau] = (ax_ray[c][ht]*pr_ray[s][ht] -
                           ax_ray[s][ht]*pr_ray[c][ht])/opt_inv
            ax_ray[c][slp] = (ax_ray[s][ht] - ax_ray[c][ht])/sys[c][tau]
            pr_ray[c][slp] = (pr_ray[s][ht] - pr_ray[c][ht])/sys[c][tau]
            sys[c][pwr] = (ax_ray[p][slp]*pr_ray[c][slp] -
                           ax_ray[c][slp]*pr_ray[p][slp])/opt_inv

            if s < nsm1:
                sys[s][pwr] = (ax_ray[c][slp]*pr_ray[s][slp] -
                               ax_ray[s][slp]*pr_ray[c][slp])/opt_inv

        else:
            ax_ray[c][slp] = ax_ray[p][slp]
            pr_ray[c][slp] = pr_ray[p][slp]
            sys[c][pwr] = 0
            sys[c][tau] = 0

    def apply_slope_dgm_data(self, surf, new_vertex=None):
        """ This routine calculates all data dependent on the input
            slope coordinates (nu,nubar) at surface surf.
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr
        opt_inv = self.opt_inv

        if new_vertex is not None:
            pr_ray[surf][slp] = new_vertex[0]
            ax_ray[surf][slp] = new_vertex[1]

        nsm1 = len(sys) - 1
        if nsm1 == 0:
            p = 0
            c = 1
            ax_ray[c][ht] = ax_ray[p][slp]*sys[p][tau] + ax_ray[p][ht]
            pr_ray[c][ht] = pr_ray[p][slp]*sys[p][tau] + pr_ray[p][ht]

        else:
            if (surf == 0):
                surf += 1

            p = surf - 1
            c = surf

            sys[c][pwr] = (ax_ray[p][slp]*pr_ray[c][slp] -
                           ax_ray[c][slp]*pr_ray[p][slp])/opt_inv
            ax_ray[c][ht] = (ax_ray[p][slp] - ax_ray[c][slp])/sys[c][pwr]
            pr_ray[c][ht] = (pr_ray[p][slp] - pr_ray[c][slp])/sys[c][pwr]
            sys[p][tau] = (ax_ray[p][ht]*pr_ray[c][ht] -
                           ax_ray[c][ht]*pr_ray[p][ht])/opt_inv

            if (surf < nsm1):
                s = surf + 1
                ax_ray[s][ht] = ax_ray[c][slp]*sys[c][tau] + ax_ray[c][ht]
                pr_ray[s][ht] = pr_ray[c][slp]*sys[c][tau] + pr_ray[c][ht]

    def update_composite_node(self, node, new_vertex=None):
        self.apply_ht_dgm_data(node, new_vertex)
        parax_model = self.opt_model['parax_model']
        if self.ifcs_mapping is not None:
            air_gap_list, node_defs, map_to_ifcs = self.ifcs_mapping
            nodes = [self.get_pt(i) for i in range(len(self.ax))]
            nodes_ifcs = calc_ifcs_nodes(map_to_ifcs, nodes)
            for i, ifcs_node in enumerate(nodes_ifcs):
            #     parax_model.set_pt(i, ifcs_node)
            # for i in range(len(nodes)):
                parax_model.apply_ht_dgm_data(i, ifcs_node)

    def update_rindex(self, surf):
        """Update the refractive index using the `gap` at *surf*."""
        gap = self.seq_model.gaps[surf]
        wvl = self.seq_model.central_wavelength()
        self.sys[surf][indx] = gap.medium.rindex(wvl)

    # ParaxTrace() - This routine performs a paraxial raytrace from object
    #                (surface 0) to image.  The last operation is a
    #                transfer to the image surface.
    def paraxial_trace(self):
        """ regenerate paraxial axial and chief rays from power and reduced
            distance
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr

        nsm1 = len(sys) - 1

        # Transfer from object
        c = 0
        s = 1
        ax_ray[s][ht] = ax_ray[c][ht] + sys[c][tau]*ax_ray[c][slp]
        pr_ray[s][ht] = pr_ray[c][ht] + sys[c][tau]*pr_ray[c][slp]

        for i in range(1, len(sys)):

            p = c
            c = s

            # Refraction
            ax_ray[c][slp] = ax_ray[p][slp] - ax_ray[c][ht]*sys[c][pwr]
            pr_ray[c][slp] = pr_ray[p][slp] - pr_ray[c][ht]*sys[c][pwr]

            # Transfer
            if (i < nsm1):
                s += 1
                ax_ray[s][ht] = ax_ray[c][ht] + sys[c][tau]*ax_ray[c][slp]
                pr_ray[s][ht] = pr_ray[c][ht] + sys[c][tau]*pr_ray[c][slp]

    # --- list output
    def list_lens(self):
        """ list the paraxial axial and chief rays, and power, reduced distance
        """
        sys = self.sys
        ax_ray = self.ax
        pr_ray = self.pr

        print("       ax_ray_ht    ax_ray_slp")
        for i in range(0, len(ax_ray)):
            print("{:2}: {:12.6g}  {:12.6g}".format(i, ax_ray[i][ht],
                                                    ax_ray[i][slp]))

        print("\n       pr_ray_ht    pr_ray_slp")
        for i in range(0, len(pr_ray)):
            print("{:2}: {:12.6g}  {:12.6g}".format(i, pr_ray[i][ht],
                                                    pr_ray[i][slp]))

        print("\n            power           tau        index    type")
        for i in range(0, len(sys)):
            print("{:2}: {:13.7g}  {:12.5g} {:12.5f}    {}".format(
                i, sys[i][pwr], sys[i][tau], sys[i][indx], sys[i][rmd]))

    def list_sys_seq(self):
        print("             c            t        medium     mode")
        fmt = "{:2}: {:12.7g} {:#12.6g} {:12.5f} {:>10s}"
        sys = self.sys
        n_before = sys[0][indx]
        for i, sg in enumerate(self.sys):
            n_after = sys[i][indx]
            thi = n_after*sys[i][tau]
            delta_n = n_after - n_before
            cv = sys[i][pwr] if delta_n == 0 else sys[i][pwr]/delta_n
            print(fmt.format(i, cv, thi, n_after, sys[i][rmd]))
            n_before = n_after

    def first_order_data(self):
        """List out the first order imaging properties of the model."""
        self.opt_model.optical_spec.parax_data.fod.list_first_order_data()

    # --- convert to/from sequential model
    def seq_path_to_paraxial_lens(self, path):
        """ returns lists of power, reduced thickness, signed index and refract
            mode
        """
        sys = []
        for i, sg in enumerate(path):
            ifc, gap, _, rndx, z_dir = sg
            imode = ifc.interact_mode
            power = ifc.optical_power
            if gap:
                n_after = rndx if z_dir > 0 else -rndx
                tau = gap.thi/n_after
                sys.append([power, tau, n_after, imode])
            else:
                sys.append([power, 0.0, sys[-1][indx], imode])
        return sys

    def paraxial_lens_to_seq_model(self):
        """ Applies a paraxial lens spec (power, reduced distance) to the model
        """
        sys = self.sys
        ax_ray = self.ax
        n_before = sys[0][indx]
        slp_before = self.ax[0][slp]
        for i, sg in enumerate(self.seq_model.path()):
            ifc, gap, _, _, _ = sg
            if gap:
                n_after = sys[i][indx]
                slp_after = ax_ray[i][slp]
                gap.thi = n_after*sys[i][tau]

                ifc.set_optical_power(sys[i][pwr], n_before, n_after)
                ifc.from_first_order(slp_before, slp_after, ax_ray[i][ht])

                n_before = n_after
                slp_before = slp_after

    # --- power and thickness solves
    def pwr_slope_solve(self, ray, surf, slp_new):
        p = ray[surf-1]
        c = ray[surf]
        pwr = (p[slp] - slp_new)/c[ht]
        return pwr

    def pwr_ht_solve(self, ray, surf, ht_new):
        sys = self.sys
        p = ray[surf-1]
        c = ray[surf]
        slp_new = (ht_new - c[ht])/sys[surf][tau]
        pwr = (p[slp] - slp_new)/ht_new
        return pwr

    def thi_ht_solve(self, ray, surf, ht_new):
        c = ray[surf]
        thi = (ht_new - c[ht])/c[slp]
        return thi

    # --- calculations
    def compute_principle_points(self, seq):
        """ Returns paraxial p and q rays, plus partial first order data.

        Args:
            seq: a sequence containing interfaces and gaps to be traced.
                  for each iteration, the sequence should return a
                  list containing: **Intfc, Gap, Trfm, Index, Z_Dir**

        Returns:
            (p_ray, q_ray, (efl, pp1, ppk, ffl, bfl))

            - p_ray: [ht, slp, aoi], [1, 0, -]
            - q_ray: [ht, slp, aoi], [0, 1, -]
            - efl: effective focal length
            - pp1: distance of front principle plane from 1st interface
            - ppk: distance of rear principle plane from last interface
            - ffl: front focal length
            - bfl: back focal length
        """
        n_0 = seq[0][mc.Indx]
        z_dir_before = seq[0][mc.Zdir]
        n_k = seq[-1][mc.Indx]
        z_dir_k = seq[-1][mc.Zdir]
        path = [[Surface(), Gap(), None, n_0, z_dir_before]]
        path.extend(seq[1:])
        pp_info = fo.compute_principle_points(iter(path),
                                              n_0=z_dir_before*n_0,
                                              n_k=z_dir_k*n_k)
        return pp_info

    def paraxial_vignetting(self, rel_fov=1):
        """Calculate the vignetting factors using paraxial optics. """
        sm = self.seq_model
        min_vly = 1, None
        min_vuy = 1, None
        for i, ifc in enumerate(sm.ifcs[:-1]):
            if self.ax[i][mc.ht] != 0:
                max_ap = ifc.surface_od()
                y = self.ax[i][mc.ht]
                ybar = rel_fov * self.pr[i][mc.ht]
                ratio = (max_ap - abs(ybar))/abs(y)
                if ratio > 0:
                    if ybar < 0:
                        if ratio < min_vly[0]:
                            min_vly = ratio, i
                    else:
                        if ratio < min_vuy[0]:
                            min_vuy = ratio, i
                # print(f'{i:2d}: {ratio:8.3f} {ybar:8.3f} {y:8.3f} {max_ap:8.3f}')

        # print("min_vly:", min_vly, "min_vuy:", min_vuy)
        return min_vly, min_vuy


def create_diagram_for_key(opm, key):
    if key == 'eles':
        air_gap_list = gen_air_gap_list(opm, '#airgap')
    elif key == 'sys':
        air_gap_list = [0, -1]
    else:
        return 'ifcs', opm.parax_model

    # nodes, node_def = gen_yybar(opm['parax_model'], air_gap_list)
    node_defs = air_gaps_to_node_defs(air_gap_list)
    nodes = nodes_from_node_defs(opm['parax_model'], node_defs)
    map_to_ifcs = gen_ifcs_node_mapping(opm['parax_model'], node_defs, nodes)
    ifcs_mapping = air_gap_list, node_defs, map_to_ifcs
    prx_model = build_from_yybar(opm, nodes, ifcs_mapping)
    return key, prx_model    


def gen_air_gap_list(opm, tag):
    air_nodes = opm['pt'].nodes_with_tag(tag)
    air_gap_list = [n.id.reference_idx() for n in air_nodes]
    return air_gap_list


def air_gaps_to_node_defs(air_gap_list):
    prev_gap_idx = 0
    node_defs = [(prev_gap_idx,)]
    for gap_idx in air_gap_list[1:]:
        node_defs.append((prev_gap_idx, gap_idx))
        prev_gap_idx = gap_idx
    node_defs.append((gap_idx+1,))
    return node_defs


def nodes_from_node_defs(parax_model, node_defs):
    nodes = []
    for i, kernel in enumerate(node_defs):
        if len(kernel) == 1:
            nodes.append(parax_model.get_pt(kernel[0]))
        elif len(kernel) == 2:
            prev_gap_idx, gap_idx = kernel
            l1_pt1 = parax_model.get_pt(prev_gap_idx)
            l1_pt2 = parax_model.get_pt(prev_gap_idx+1)
            l2_pt1 = parax_model.get_pt(gap_idx)
            l2_pt2 = parax_model.get_pt(gap_idx+1)
            new_node = get_intersect(l1_pt1, l1_pt2, l2_pt1, l2_pt2)
            nodes.append(new_node)
    return nodes


def gen_ifcs_node_mapping(parax_model, node_defs, nodes):
    """Create mapping between composite diagram and interface based diagram.
    
    I think this works only for singlets and mirrors.
    """
    map_to_ifcs = []
    origin = np.array([0., 0.])
    for i, kernel in enumerate(node_defs):
        if len(kernel) == 1:
            idx = kernel[0]
            map_to_ifcs.append((idx, i, 0.))
        elif len(kernel) == 2:
            l1_pt1 = np.array(nodes[i-1])
            l1_pt2 = np.array(nodes[i])
            l2_pt1 = np.array(nodes[i])
            l2_pt2 = np.array(nodes[i+1])
            
            prev_gap_idx, gap_idx = kernel
            for k in range(prev_gap_idx+1, gap_idx+1):
                pt_k = np.array(parax_model.get_pt(k))
                new_node1 = np.array(get_intersect(l1_pt1, l1_pt2,
                                                   origin, pt_k))
                if np.allclose(new_node1, pt_k):
                    t1 = norm(new_node1 - l1_pt1)/norm(l1_pt2 - l1_pt1)
                    map_to_ifcs.append((k, i-1, t1))
                else:
                    new_node2 = np.array(get_intersect(origin, pt_k,
                                                       l2_pt1, l2_pt2))
                    if np.allclose(new_node2, pt_k):
                        t2 = norm(new_node2 - l2_pt1)/norm(l2_pt2 - l2_pt1)
                        map_to_ifcs.append((k, i, t2))
    return map_to_ifcs


def build_from_yybar(opm, nodes, ifcs_mapping):
    prx_model = ParaxialModel(opm, opt_inv=opm['pm'].opt_inv,
                              ifcs_mapping=ifcs_mapping)
    for vertex in nodes:
        prx_model.ax.append([vertex[1], 0.0, 0.0])
        prx_model.pr.append([vertex[0], 0.0, 0.0])
        prx_model.sys.append([0.0, 0.0, 1, 'transmit'])
    prx_model.sys[0][rmd] = 'dummy'
    prx_model.sys[-1][rmd] = 'dummy'

    for i in range(len(nodes)):
        prx_model.apply_ht_dgm_data(i)
    
    return prx_model


def calc_ifcs_nodes(map_to_ifcs, nodes):
    """Given a composite diagram, calculate the interface based diagram. """
    nodes_ifcs = []
    for i, kernel in enumerate(map_to_ifcs):
        idx, nidx, t = kernel
        if t == 0:
            new_node = np.array(nodes[nidx])
        else:
            l1_pt1 = np.array(nodes[nidx])
            l1_pt2 = np.array(nodes[nidx+1])
            new_node = t*(l1_pt2 - l1_pt1) + l1_pt1
        nodes_ifcs.append(new_node)
    return nodes_ifcs
