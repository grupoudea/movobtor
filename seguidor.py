import math


class Seguidor:

    def __init__(self):
        self.id_count = 0
        self.centro_puntos = {}

    def rastrear(self, objetoCordenada):

        objetos_id = []

        for obj in objetoCordenada:
            x, y, w, h = obj

            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            object_det = False
            for id, pt in self.centro_puntos.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.centro_puntos[id] = (cx, cy)
                    objetos_id.append([x, y, w, h, id])
                    object_det = True
                    break

            if object_det is False:
                self.centro_puntos[self.id_count] = (cx, cy)
                objetos_id.append([x, y, w, h, self.id_count])
                self.id_count = self.id_count + 1

        new_center_points = {}
        for obj_bb_id in objetos_id:
            _, _, _, _, object_id = obj_bb_id

            center = self.centro_puntos[object_id]
            new_center_points[object_id] = center

        self.centro_puntos = new_center_points.copy()
        return objetos_id
