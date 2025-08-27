# Imports:
# --------
import numpy as np


# Function: Inverts Transformation matrix
# ---------
def invert_T(T):
    R = T[:3,:3]
    t = T[:3, 3]
    T_inv = np.eye(4)
    T_inv[:3,:3] = R.T
    T_inv[:3, 3] = -R.T @ t
    
    return T_inv


# Function: Convert Rotation to Roll, Pitch, Yaw format
# ---------
def rpy_from_R(R):
    sy = np.sqrt(R[0,0]**2 + R[1,0]**2)

    if sy > 1e-6:
        # No gimal lock
        roll  = np.arctan2(R[2,1], R[2,2])
        pitch = np.arctan2(-R[2,0], sy)
        yaw   = np.arctan2(R[1,0], R[0,0])
    else:
        # With gimbal lock
        # TODO: Decide between roll=0 or yaw=0
        roll  = np.arctan2(-R[1,2], R[1,1])
        pitch = np.arctan2(-R[2,0], sy)
        yaw   = 0.0
    return float(roll), float(pitch), float(yaw)


# Function: Converts T matrix to (x,y,z) and (roll, pitch, yaw)
# ---------
def xyz_rpy_from_T(T_adma_to_sensor):
    R = T_adma_to_sensor[:3,:3]
    t = T_adma_to_sensor[:3, 3]

    r,p,y = rpy_from_R(R)

    return (float(t[0]), float(t[1]), float(t[2])), (r,p,y)


# Main Function: Gets (x,y,z, roll, pitch, yaw) from T matrix
# --------------
def get_info(T: np.ndarray,
             adma_to_sensor: bool=True):

    if not adma_to_sensor:
        T = invert_T(T)

    (x,y,z), (r,p,yaw) = xyz_rpy_from_T(T)

    print("translation:", [round(x,6), round(y,6), round(z,6)])
    print("rotation_rpy:", [round(r,6), round(p,6), round(yaw,6)])


# Run as script:
# --------------
if __name__ == "__main__":
    T = np.array([
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    
    get_info(T=T, 
             adma_to_sensor=True)
