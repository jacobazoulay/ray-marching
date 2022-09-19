import cv2
import numpy as np


SPHERE = np.array([100, 200, 200])
RADIUS = 20


def sdSphere(pt):
    sphere = SPHERE
    r = RADIUS
    dist = np.linalg.norm(pt - sphere) - r
    return dist


def raymarch(ray, ray_org):
    dist = 0
    for i in range(255):
        pt = ray_org + ray * dist
        dist += np.linalg.norm(pt - SPHERE) - RADIUS
        sdf = sdSphere(pt)
        if sdf < 1:
            hit = True
            return hit, pt
        elif sdf > 1000:
            hit = False
            return hit, pt
    return False, pt


def calc_diffuse(pt, pt_norm, light_org):
    light_ray = light_org - pt
    light_ray = light_ray / np.linalg.norm(light_ray)
    shade_factor = np.maximum(np.dot(pt_norm, light_ray), 0.0)
    return shade_factor


def calc_norm(pt):
    sphere = SPHERE
    norm = pt - sphere
    norm = norm / np.linalg.norm(norm)
    return norm


def main():
    img = np.zeros((300, 400, 3), dtype='uint8')
    ray_org = np.array([150, 250, -100])
    light_org = np.array([-100, 150, -400])

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            # (y, x) = 130, 234
            ray = np.array([y, x, 0]) - ray_org
            ray = ray / np.linalg.norm(ray)
            hit, pt = raymarch(ray, ray_org)
            if hit:
                pt_norm = calc_norm(pt)
                shade_factor = calc_diffuse(pt, pt_norm, light_org,)
                img[y, x, :] = np.array([100, 210, 255]) * shade_factor
            else:
                img[y, x, :] = np.array([230, 230, 230])
    cv2.imshow("Display", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()