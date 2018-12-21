import math
import numpy as np


class RationalBezier(object):
    def __init__(self, arc, tstart=0, tend=1):
        self.start = arc.point(tstart)
        self.end = arc.point(tend)

        s_tangentc = arc.unit_tangent(tstart)
        e_tangentc = arc.unit_tangent(tend)


        s_tangent = (arc.tf.dot(  np.array([[s_tangentc.real], [s_tangentc.imag], [0.0]])))
        e_tangent = (arc.tf.dot(  np.array([[e_tangentc.real], [e_tangentc.imag], [0.0]])))

        self.weights = np.array([1., math.cos((tend-tstart)*arc.delta/180.*math.pi/2.), 1.])

        sx = self.start.real
        sy = self.start.imag

        ex = self.end.real
        ey = self.end.imag

        stx = s_tangent[0]
        sty = s_tangent[1]
        stn = math.sqrt(stx**2+sty**2)
        stx /= stn
        sty /= stn


        etx = e_tangent[0]
        ety = e_tangent[1]
        etn = math.sqrt(etx**2+ety**2)
        etx /= -etn
        ety /= -etn

        px = (((ey-sy)*stx+sty*sx)*etx-ety*ex*stx)/(etx*sty-ety*stx)
        py = (((-ex+sx)*sty-stx*sy)*ety+etx*ey*sty)/(etx*sty-ety*stx)

        self.control = px[0] + 1j*py[0]

    def __repr__(self):
        params = (self.start, self.control, self.end, self.weights)
        return ("RationalBezier(start={}, control={}, end={}, w={})".format(*params))

    def __eq__(self, other):
        if not isinstance(other, RationalBezier):
            return NotImplemented
        return self.start == other.start and self.end == other.end \
            and self.control == other.control \
            and self.weights == other.weights

    def __ne__(self, other):
        if not isinstance(other, RationalBezier):
            return NotImplemented
        return not self == other

    def point(self, t):
        b0=(1-t)**2
        b1=2*(1-t)*t
        b2=t**2

        c0x = self.start.real
        c0y = self.start.imag

        c1x = self.control.real
        c1y = self.control.imag

        c2x = self.end.real
        c2y = self.end.imag

        denom = b0*self.weights[0]+b1*self.weights[1]+b2*self.weights[2]

        vx = (b0*c0x*self.weights[0]+b1*c1x*self.weights[1]+b2*c2x*self.weights[2])/denom
        vy = (b0*c0y*self.weights[0]+b1*c1y*self.weights[1]+b2*c2y*self.weights[2])/denom

        return vx + 1j*vy
