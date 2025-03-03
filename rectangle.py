class RoundedRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Initialize a rounded rectangle

        Args:
            canvas: The tkinter canvas to draw on
            x1, y1: Top-left corner coordinates
            x2, y2: Bottom-right corner coordinates
            radius: Corner radius (default: 25)
            **kwargs: Additional arguments to pass to canvas.create_polygon
        """
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.radius = radius
        self.kwargs = kwargs
        self.shape_id = None

    def draw(self):
        """Draw the rounded rectangle on the canvas

        Returns:
            The ID of the created polygon
        """
        points = [
            self.x1 + self.radius, self.y1,
            self.x2 - self.radius, self.y1,
            self.x2, self.y1,
            self.x2, self.y1 + self.radius,
            self.x2, self.y2 - self.radius,
            self.x2, self.y2,
            self.x2 - self.radius, self.y2,
            self.x1 + self.radius, self.y2,
            self.x1, self.y2,
            self.x1, self.y2 - self.radius,
            self.x1, self.y1 + self.radius,
            self.x1, self.y1
        ]

        self.shape_id = self.canvas.create_polygon(points, smooth=True, **self.kwargs)
        return self.shape_id

    def config(self, **kwargs):
        """Update the configuration of the rounded rectangle

        Args:
            **kwargs: New configuration settings
        """
        if self.shape_id:
            self.canvas.itemconfig(self.shape_id, **kwargs)
            # Update stored kwargs for future reference
            for key, value in kwargs.items():
                self.kwargs[key] = value

    def move(self, dx, dy):
        """Move the rounded rectangle

        Args:
            dx: Horizontal distance to move
            dy: Vertical distance to move
        """
        if self.shape_id:
            self.canvas.move(self.shape_id, dx, dy)
            # Update coordinates
            self.x1 += dx
            self.y1 += dy
            self.x2 += dx
            self.y2 += dy

    def get_id(self):
        """Get the canvas ID of the shape

        Returns:
            The ID of the created polygon
        """
        return self.shape_id