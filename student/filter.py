# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        dim_v = int(params.dim_state/2)
        F = np.identity(params.dim_state)
        F[0:dim_v,dim_v:] = np.identity(dim_v)*params.dt
        return np.matrix(F)
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############

        dim_v = int(params.dim_state/2)
        dt = params.dt
        q = params.q
        noise_p = (dt**3/3)*q
        noise_cross = (dt**2/2)*q
        noise_v = dt*q
        Q = np.identity(params.dim_state)
        Q[0:dim_v,0:dim_v] = np.identity(dim_v)*noise_p
        Q[dim_v:,dim_v:]   = np.identity(dim_v)*noise_v
        Q[0:dim_v,dim_v:]  = np.identity(dim_v)*noise_cross
        Q[dim_v:,0:dim_v]  = np.identity(dim_v)*noise_cross
        return np.matrix(Q)
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        F = self.F()
        Q = self.Q()
        
        x = F*track.x
        p = F*track.P* F.transpose() +Q
        
        track.set_x(x)
        track.set_P(p)
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        x_pred = track.x
        p_pred = track.P
        
        #retrive Jacobian matrix at current prediction result
        H = meas.sensor.get_H(x_pred)
        
        #retrive value of (real meas - cur pred)
        gamma = self.gamma(track,meas)
        
        S = self.S(track,meas,H)
        
        K = p_pred * H.transpose() * np.linalg.inv(S)
        
        x = x_pred + K*gamma
        
        I = np.identity(params.dim_state)
        
        #update covariance P
        
        p = (I - K*H)*p_pred
        
        
        track.set_x(x)
        track.set_P(p)
        
        
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        gamma = meas.z - meas.sensor.get_hx(track.x)
        return gamma
        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        S = (H *track.P *H.transpose()) + meas.R
        return S
        
        ############
        # END student code
        ############ 