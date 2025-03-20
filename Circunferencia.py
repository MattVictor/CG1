import math

class Circunferencia():
    def __init__(self):
        self.currentFunction = self.pontoMedio
        
    def drawFunction(self, clicked_points, circle_center=False,circle_radius=False):
        if len(clicked_points) == 4:
            x1, y1 = clicked_points[0], clicked_points[1]
            x2, y2 = clicked_points[2], clicked_points[3]
        
        if not circle_center:
            circle_center = [x1, y1]
            
        if not circle_radius:
            circle_radius = math.sqrt(((x2 - x1)**2) + ((y2-y1)**2))
            circle_radius = round(circle_radius)
        
        return self.currentFunction(circle_center, circle_radius)
    
    def pontoMedio(self, circle_center,circle_radius):
        lighted_pixels = []
        
        xc, yc = circle_center[0], circle_center[1]

        R = circle_radius
        
        x = 0
        y = R
        d = 1 - R  # Variável de decisão inicial]
        
        def plot_circle_points(x, y):                
            points = [
                (xc + x, yc + y), (xc + y, yc + x),
                (xc + y, yc - x), (xc + x, yc - y),
                (xc - x, yc - y), (xc - y, yc - x),
                (xc - y, yc + x), (xc - x, yc + y)
            ]
            for px, py in points:
                lighted_pixels.append((px, py))
        
        plot_circle_points(x, y)
        
        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
            plot_circle_points(x, y)
        
        return lighted_pixels