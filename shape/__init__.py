
# https://desk.draw.io/support/solutions/articles/16000052874-how-to-create-and-edit-shapes-
import string


class Shape(object):
    height = 46  # 100
    width = 61  # 100
    aspect = "fixed"
    strokewidth = "1"
    spacing = 2.54  # mm
    hole_size = 1.5
    board_color = "#99bda8"
    pad_color = "#d0d0d0"
    pad_hole_color = "#6b6b6b"

    aspect_ratio = 0.0
    axis_chars = list(string.ascii_uppercase)

    def __init__(self, attrs=dict()):
        if "height" in attrs:
            self.height = attrs["height"]
        if "width" in attrs:
            self.width = attrs["width"]
        if "aspect" in attrs:
            self.aspect = attrs["aspect"]
        if "strokewidth" in attrs:
            self.strokewidth = attrs["strokewidth"]
        if "spacing" in attrs:
            self.strokewidth = attrs["spacing"]

        self.aspect_ratio = self.width / self.height

    def render_connections(self):
        connections = "  <connections>\n"
        pads = ""
        labels = ""
        half_space = self.spacing / 2.0

        x = half_space
        y = half_space
        row = 0
        while y < self.height - half_space:
            # row labels
            labels += f'    <text str="{self.axis_chars[row % len(self.axis_chars)]}" align="right" x="-1" y="{0.1+y-half_space}"/>\n'
            col = 0
            while x < self.width - half_space:
                conn_x = (1.0 / self.width * (x+0.1))
                conn_y = (1.0 / self.height * (y+0.1))
                connections += f'    <constraint x="{conn_x}" y="{conn_y}" perimeter="0" name="{round(x, 2)},{round(y, 2)}"/>\n'

                pad_x = x - half_space / 2.0
                pad_y = y - half_space / 2.0
                pad_w = self.hole_size
                pad_h = self.hole_size
                pads += f'    <ellipse x="{pad_x}" y="{pad_y}" w="{pad_w}" h="{pad_h}"/><fillstroke/>\n'

                if row == 0:
                    # column labels
                    labels += f'    <text str="{self.axis_chars[col % len(self.axis_chars)]}" align="center" valign="bottom" x="{0.6+pad_x}" y="{pad_y-1}"/>'

                x += self.spacing
                col += 1
            y += self.spacing
            x = half_space
            row += 1
        connections += "  </connections>"
        return connections, pads, labels

    def render(self):
        connections, pads, labels = self.render_connections()

        return f"""<shape h = "{self.height}" w = "{self.width}" aspect = "{self.aspect}" strokewidth = "{self.strokewidth}" >
{connections}
  <background >
    <strokecolor color="{self.board_color}"/>
    <fillcolor color="{self.board_color}"/>
    <rect x="0" y="0" w="{self.width}" h="{self.height}"/>
    <fontcolor color="#000000"/>
    <fontsize size="2"/>
    <fontfamily family="Courier New"/>
  </background >
  <foreground >
    <fillstroke/>
    <save/>
    <save/>
    <save/>
    <save/>
    <save/>
    <save/>
    <save/>
    <strokecolor color="{self.pad_color}"/>
    <fillcolor color="{self.pad_hole_color}"/>
{labels}
    <strokewidth width="0.7"/>
{pads}
  </foreground >
</shape >"""
