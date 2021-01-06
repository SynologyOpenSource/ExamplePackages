# vim: set fileencoding=utf-8 :

# ***********************IMPORTANT NMAP LICENSE TERMS************************
# *                                                                         *
# * The Nmap Security Scanner is (C) 1996-2020 Insecure.Com LLC ("The Nmap  *
# * Project"). Nmap is also a registered trademark of the Nmap Project.     *
# *                                                                         *
# * This program is distributed under the terms of the Nmap Public Source   *
# * License (NPSL). The exact license text applying to a particular Nmap    *
# * release or source code control revision is contained in the LICENSE     *
# * file distributed with that version of Nmap or source code control       *
# * revision. More Nmap copyright/legal information is available from       *
# * https://nmap.org/book/man-legal.html, and further information on the    *
# * NPSL license itself can be found at https://nmap.org/npsl. This header  *
# * summarizes some key points from the Nmap license, but is no substitute  *
# * for the actual license text.                                            *
# *                                                                         *
# * Nmap is generally free for end users to download and use themselves,    *
# * including commercial use. It is available from https://nmap.org.        *
# *                                                                         *
# * The Nmap license generally prohibits companies from using and           *
# * redistributing Nmap in commercial products, but we sell a special Nmap  *
# * OEM Edition with a more permissive license and special features for     *
# * this purpose. See https://nmap.org/oem                                  *
# *                                                                         *
# * If you have received a written Nmap license agreement or contract       *
# * stating terms other than these (such as an Nmap OEM license), you may   *
# * choose to use and redistribute Nmap under those terms instead.          *
# *                                                                         *
# * The official Nmap Windows builds include the Npcap software             *
# * (https://npcap.org) for packet capture and transmission. It is under    *
# * separate license terms which forbid redistribution without special      *
# * permission. So the official Nmap Windows builds may not be              *
# * redistributed without special permission (such as an Nmap OEM           *
# * license).                                                               *
# *                                                                         *
# * Source is provided to this software because we believe users have a     *
# * right to know exactly what a program is going to do before they run it. *
# * This also allows you to audit the software for security holes.          *
# *                                                                         *
# * Source code also allows you to port Nmap to new platforms, fix bugs,    *
# * and add new features.  You are highly encouraged to submit your         *
# * changes as a Github PR or by email to the dev@nmap.org mailing list     *
# * for possible incorporation into the main distribution. Unless you       *
# * specify otherwise, it is understood that you are offering us very       *
# * broad rights to use your submissions as described in the Nmap Public    *
# * Source License Contributor Agreement. This is important because we      *
# * fund the project by selling licenses with various terms, and also       *
# * because the inability to relicense code has caused devastating          *
# * problems for other Free Software projects (such as KDE and NASM).       *
# *                                                                         *
# * The free version of Nmap is distributed in the hope that it will be     *
# * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Warranties,        *
# * indemnification and commercial support are all available through the    *
# * Npcap OEM program--see https://nmap.org/oem.                            *
# *                                                                         *
# ***************************************************************************/

import gtk
import math
import gobject

import radialnet.util.geometry as geometry

from radialnet.bestwidgets.boxes import *
from radialnet.core.Coordinate import PolarCoordinate
import radialnet.gui.RadialNet as RadialNet
from radialnet.bestwidgets.expanders import BWExpander


OPTIONS = ['address',
           'hostname',
           'icon',
           'latency',
           'ring',
           'region',
           'slow in/out']

REFRESH_RATE = 500


class ControlWidget(BWVBox):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWVBox.__init__(self)
        self.set_border_width(6)

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__action = ControlAction(self.radialnet)
        self.__interpolation = ControlInterpolation(self.radialnet)
        self.__layout = ControlLayout(self.radialnet)
        self.__view = ControlView(self.radialnet)

        self.bw_pack_start_noexpand_nofill(self.__action)
        self.bw_pack_start_noexpand_nofill(self.__interpolation)
        self.bw_pack_start_noexpand_nofill(self.__layout)
        self.bw_pack_start_noexpand_nofill(self.__view)


def try_set_tooltip_text(widget, text):
    try:
        widget.set_tooltip_text(text)
    except AttributeError:
        # The set_tooltip_text method was introduced in PyGTK 2.12.
        pass


class ControlAction(BWExpander):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWExpander.__init__(self, _('Action'))
        self.set_expanded(True)

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__tbox = BWTable(1, 4)
        self.__tbox.bw_set_spacing(0)
        self.__vbox = BWVBox()

        self.__jump_to = gtk.RadioToolButton(None, gtk.STOCK_JUMP_TO)
        try_set_tooltip_text(self.__jump_to, 'Change focus')
        self.__jump_to.connect('toggled',
                               self.__change_pointer,
                               RadialNet.POINTER_JUMP_TO)

        try:
            # gtk.STOCK_INFO is available only in PyGTK 2.8 and later.
            info_icon = gtk.STOCK_INFO
        except AttributeError:
            self.__info = gtk.RadioToolButton(self.__jump_to, None)
            self.__info.set_label(_("Info"))
        else:
            self.__info = gtk.RadioToolButton(self.__jump_to, info_icon)
        try_set_tooltip_text(self.__info, 'Show information')
        self.__info.connect('toggled',
                            self.__change_pointer,
                            RadialNet.POINTER_INFO)

        self.__group = gtk.RadioToolButton(self.__jump_to, gtk.STOCK_ADD)
        try_set_tooltip_text(self.__group, 'Group children')
        self.__group.connect('toggled',
                             self.__change_pointer,
                             RadialNet.POINTER_GROUP)

        self.__region = gtk.RadioToolButton(self.__jump_to,
                                            gtk.STOCK_SELECT_COLOR)
        try_set_tooltip_text(self.__region, 'Fill region')
        self.__region.connect('toggled',
                              self.__change_pointer,
                              RadialNet.POINTER_FILL)

        self.__region_color = gtk.combo_box_new_text()
        self.__region_color.append_text(_('Red'))
        self.__region_color.append_text(_('Yellow'))
        self.__region_color.append_text(_('Green'))
        self.__region_color.connect('changed', self.__change_region)
        self.__region_color.set_active(self.radialnet.get_region_color())

        self.__tbox.bw_attach_next(self.__jump_to)
        self.__tbox.bw_attach_next(self.__info)
        self.__tbox.bw_attach_next(self.__group)
        self.__tbox.bw_attach_next(self.__region)

        self.__vbox.bw_pack_start_noexpand_nofill(self.__tbox)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__region_color)

        self.bw_add(self.__vbox)

        self.__jump_to.set_active(True)
        self.__region_color.set_no_show_all(True)
        self.__region_color.hide()

    def __change_pointer(self, widget, pointer):
        """
        """
        if pointer != self.radialnet.get_pointer_status():
            self.radialnet.set_pointer_status(pointer)

        if pointer == RadialNet.POINTER_FILL:
            self.__region_color.show()
        else:
            self.__region_color.hide()

    def __change_region(self, widget):
        """
        """
        self.radialnet.set_region_color(self.__region_color.get_active())


class ControlVariableWidget(gtk.DrawingArea):
    """
    """
    def __init__(self, name, value, update, increment=1):
        """
        """
        gtk.DrawingArea.__init__(self)

        self.__variable_name = name
        self.__value = value
        self.__update = update
        self.__increment_pass = increment

        self.__radius = 6
        self.__increment_time = 100

        self.__pointer_position = 0
        self.__active_increment = False

        self.__last_value = self.__value()

        self.connect('expose_event', self.expose)
        self.connect('button_press_event', self.button_press)
        self.connect('button_release_event', self.button_release)
        self.connect('motion_notify_event', self.motion_notify)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.MOTION_NOTIFY |
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

        gobject.timeout_add(REFRESH_RATE, self.verify_value)

    def verify_value(self):
        """
        """
        if self.__value() != self.__last_value:
            self.__last_value = self.__value()

        self.queue_draw()

        return True

    def button_press(self, widget, event):
        """
        """
        self.__active_increment = False
        pointer = self.get_pointer()

        if self.__button_is_clicked(pointer) and event.button == 1:

            event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.__active_increment = True
            self.__increment_value()

    def button_release(self, widget, event):
        """
        """
        event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

        self.__active_increment = False
        self.__pointer_position = 0

        self.queue_draw()

    def motion_notify(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        if self.__active_increment:

            xc, yc = self.__center_of_widget
            x, _ = self.get_pointer()

            if x - self.__radius > 0 and x + self.__radius < 2 * xc:
                self.__pointer_position = x - xc

        self.queue_draw()

    def expose(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        self.set_size_request(100, 30)

        self.context = widget.window.cairo_create()
        self.__draw()

        return True

    def __draw(self):
        """
        """
        allocation = self.get_allocation()

        self.__center_of_widget = (allocation.width / 2,
                                   allocation.height / 2)

        xc, yc = self.__center_of_widget

        # draw line
        self.context.set_line_width(1)
        self.context.set_dash([1, 2])
        self.context.move_to(self.__radius,
                             yc + self.__radius)
        self.context.line_to(2 * xc - 5,
                             yc + self.__radius)
        self.context.stroke()

        # draw text
        self.context.set_dash([1, 0])
        self.context.set_font_size(10)

        self.context.move_to(5, yc - self.__radius)
        self.context.show_text(self.__variable_name)

        width = self.context.text_extents(str(self.__value()))[2]
        self.context.move_to(2 * xc - width - 5, yc - self.__radius)
        self.context.show_text(str(self.__value()))

        self.context.set_line_width(1)
        self.context.stroke()

        # draw node
        self.context.arc(xc + self.__pointer_position,
                         yc + self.__radius,
                         self.__radius, 0, 2 * math.pi)
        if self.__active_increment:
            self.context.set_source_rgb(0.0, 0.0, 0.0)
        else:
            self.context.set_source_rgb(1.0, 1.0, 1.0)
        self.context.fill_preserve()
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.stroke()

    def __button_is_clicked(self, pointer):
        """
        """
        xc, yc = self.__center_of_widget
        center = (xc, yc + self.__radius)

        return geometry.is_in_circle(pointer, 6, center)

    def __increment_value(self):
        """
        """
        self.__update(self.__value() + self.__pointer_position / 4)

        self.queue_draw()

        if self.__active_increment:

            gobject.timeout_add(self.__increment_time,
                                self.__increment_value)

    def set_value_function(self, value):
        """
        """
        self.__value = value

    def set_update_function(self, update):
        """
        """
        self.__update = update


class ControlVariable(BWHBox):
    """
    """
    def __init__(self, name, get_function, set_function, increment=1):
        """
        """
        BWHBox.__init__(self, spacing=0)

        self.__increment_pass = increment
        self.__increment_time = 200
        self.__increment = False

        self.__name = name
        self.__get_function = get_function
        self.__set_function = set_function

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__control = ControlVariableWidget(self.__name,
                                               self.__get_function,
                                               self.__set_function,
                                               self.__increment_pass)

        self.__left_button = gtk.Button()
        self.__left_button.set_size_request(20, 20)
        self.__left_arrow = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_NONE)
        self.__left_button.add(self.__left_arrow)
        self.__left_button.connect('pressed',
                                   self.__pressed,
                                   -self.__increment_pass)
        self.__left_button.connect('released', self.__released)

        self.__right_button = gtk.Button()
        self.__right_button.set_size_request(20, 20)
        self.__right_arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_NONE)
        self.__right_button.add(self.__right_arrow)
        self.__right_button.connect('pressed',
                                    self.__pressed,
                                    self.__increment_pass)
        self.__right_button.connect('released', self.__released)

        self.bw_pack_start_noexpand_nofill(self.__left_button)
        self.bw_pack_start_expand_fill(self.__control)
        self.bw_pack_start_noexpand_nofill(self.__right_button)

    def __pressed(self, widget, increment):
        """
        """
        self.__increment = True
        self.__increment_function(increment)

    def __increment_function(self, increment):
        """
        """
        if self.__increment:

            self.__set_function(self.__get_function() + increment)
            self.__control.verify_value()

            gobject.timeout_add(self.__increment_time,
                                self.__increment_function,
                                increment)

    def __released(self, widget):
        """
        """
        self.__increment = False


class ControlFisheye(BWVBox):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWVBox.__init__(self)
        self.set_border_width(6)

        self.radialnet = radialnet
        self.__ring_max_value = self.radialnet.get_number_of_rings()

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__params = BWHBox()

        self.__fisheye_label = gtk.Label(_('<b>Fisheye</b> on ring'))
        self.__fisheye_label.set_use_markup(True)

        self.__ring = gtk.Adjustment(0, 0, self.__ring_max_value, 0.01, 0.01)

        self.__ring_spin = gtk.SpinButton(self.__ring)
        self.__ring_spin.set_digits(2)

        self.__ring_scale = gtk.HScale(self.__ring)
        self.__ring_scale.set_size_request(100, -1)
        self.__ring_scale.set_digits(2)
        self.__ring_scale.set_value_pos(gtk.POS_LEFT)
        self.__ring_scale.set_draw_value(False)
        self.__ring_scale.set_update_policy(gtk.UPDATE_CONTINUOUS)

        self.__interest_label = gtk.Label(_('with interest factor'))
        self.__interest = gtk.Adjustment(0, 0, 10, 0.01)
        self.__interest_spin = gtk.SpinButton(self.__interest)
        self.__interest_spin.set_digits(2)

        self.__spread_label = gtk.Label(_('and spread factor'))
        self.__spread = gtk.Adjustment(0, -1.0, 1.0, 0.01, 0.01)
        self.__spread_spin = gtk.SpinButton(self.__spread)
        self.__spread_spin.set_digits(2)

        self.__params.bw_pack_start_noexpand_nofill(self.__fisheye_label)
        self.__params.bw_pack_start_noexpand_nofill(self.__ring_spin)
        self.__params.bw_pack_start_expand_fill(self.__ring_scale)
        self.__params.bw_pack_start_noexpand_nofill(self.__interest_label)
        self.__params.bw_pack_start_noexpand_nofill(self.__interest_spin)
        self.__params.bw_pack_start_noexpand_nofill(self.__spread_label)
        self.__params.bw_pack_start_noexpand_nofill(self.__spread_spin)

        self.bw_pack_start_noexpand_nofill(self.__params)

        self.__ring.connect('value_changed', self.__change_ring)
        self.__interest.connect('value_changed', self.__change_interest)
        self.__spread.connect('value_changed', self.__change_spread)

        gobject.timeout_add(REFRESH_RATE, self.__update_fisheye)

    def __update_fisheye(self):
        """
        """
        # adjust ring scale to radialnet number of nodes
        ring_max_value = self.radialnet.get_number_of_rings() - 1

        if ring_max_value != self.__ring_max_value:

            value = self.__ring.get_value()

            if value == 0 and ring_max_value != 0:
                value = 1

            elif value > ring_max_value:
                value = ring_max_value

            self.__ring.set_all(value, 1, ring_max_value, 0.01, 0.01, 0)
            self.__ring_max_value = ring_max_value

            self.__ring_scale.queue_draw()

        # check ring value
        ring_value = self.radialnet.get_fisheye_ring()

        if self.__ring.get_value() != ring_value:
            self.__ring.set_value(ring_value)

        # check interest value
        interest_value = self.radialnet.get_fisheye_interest()

        if self.__interest.get_value() != interest_value:
            self.__interest.set_value(interest_value)

        # check spread value
        spread_value = self.radialnet.get_fisheye_spread()

        if self.__spread.get_value() != spread_value:
            self.__spread.set_value(spread_value)

        return True

    def active_fisheye(self):
        """
        """
        self.radialnet.set_fisheye(True)
        self.__change_ring()
        self.__change_interest()

    def deactive_fisheye(self):
        """
        """
        self.radialnet.set_fisheye(False)

    def __change_ring(self, widget=None):
        """
        """
        if not self.radialnet.is_in_animation():
            self.radialnet.set_fisheye_ring(self.__ring.get_value())
        else:
            self.__ring.set_value(self.radialnet.get_fisheye_ring())

    def __change_interest(self, widget=None):
        """
        """
        if not self.radialnet.is_in_animation():
            self.radialnet.set_fisheye_interest(self.__interest.get_value())
        else:
            self.__interest.set_value(self.radialnet.get_fisheye_interest())

    def __change_spread(self, widget=None):
        """
        """
        if not self.radialnet.is_in_animation():
            self.radialnet.set_fisheye_spread(self.__spread.get_value())
        else:
            self.__spread.set_value(self.radialnet.get_fisheye_spread())


class ControlInterpolation(BWExpander):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWExpander.__init__(self, _('Interpolation'))

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__vbox = BWVBox()

        self.__cartesian_radio = gtk.RadioButton(None, _('Cartesian'))
        self.__polar_radio = gtk.RadioButton(
                self.__cartesian_radio, _('Polar'))
        self.__cartesian_radio.connect('toggled',
                                       self.__change_system,
                                       RadialNet.INTERPOLATION_CARTESIAN)
        self.__polar_radio.connect('toggled',
                                   self.__change_system,
                                   RadialNet.INTERPOLATION_POLAR)

        self.__system_box = BWHBox()
        self.__system_box.bw_pack_start_noexpand_nofill(self.__polar_radio)
        self.__system_box.bw_pack_start_noexpand_nofill(self.__cartesian_radio)

        self.__frames_box = BWHBox()
        self.__frames_label = gtk.Label(_('Frames'))
        self.__frames_label.set_alignment(0.0, 0.5)
        self.__frames = gtk.Adjustment(self.radialnet.get_number_of_frames(),
                                       1,
                                       1000,
                                       1)
        self.__frames.connect('value_changed', self.__change_frames)
        self.__frames_spin = gtk.SpinButton(self.__frames)
        self.__frames_box.bw_pack_start_expand_fill(self.__frames_label)
        self.__frames_box.bw_pack_start_noexpand_nofill(self.__frames_spin)

        self.__vbox.bw_pack_start_noexpand_nofill(self.__frames_box)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__system_box)

        self.bw_add(self.__vbox)

        gobject.timeout_add(REFRESH_RATE, self.__update_animation)

    def __update_animation(self):
        """
        """
        active = self.radialnet.get_interpolation()

        if active == RadialNet.INTERPOLATION_CARTESIAN:
            self.__cartesian_radio.set_active(True)

        else:
            self.__polar_radio.set_active(True)

        return True

    def __change_system(self, widget, value):
        """
        """
        if not self.radialnet.set_interpolation(value):

            active = self.radialnet.get_interpolation()

            if active == RadialNet.INTERPOLATION_CARTESIAN:
                self.__cartesian_radio.set_active(True)

            else:
                self.__polar_radio.set_active(True)

    def __change_frames(self, widget):
        """
        """
        if not self.radialnet.set_number_of_frames(self.__frames.get_value()):
            self.__frames.set_value(self.radialnet.get_number_of_frames())


class ControlLayout(BWExpander):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWExpander.__init__(self, _('Layout'))

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__hbox = BWHBox()

        self.__layout = gtk.combo_box_new_text()
        self.__layout.append_text(_('Symmetric'))
        self.__layout.append_text(_('Weighted'))
        self.__layout.set_active(self.radialnet.get_layout())
        self.__layout.connect('changed', self.__change_layout)
        self.__force = gtk.ToolButton(gtk.STOCK_REFRESH)
        self.__force.connect('clicked', self.__force_update)

        self.__hbox.bw_pack_start_expand_fill(self.__layout)
        self.__hbox.bw_pack_start_noexpand_nofill(self.__force)

        self.bw_add(self.__hbox)

        self.__check_layout()

    def __check_layout(self):
        """
        """
        if self.__layout.get_active() == RadialNet.LAYOUT_WEIGHTED:
            self.__force.set_sensitive(True)

        else:
            self.__force.set_sensitive(False)

        return True

    def __force_update(self, widget):
        """
        """
        self.__fisheye_ring = self.radialnet.get_fisheye_ring()
        self.radialnet.update_layout()

    def __change_layout(self, widget):
        """
        """
        if not self.radialnet.set_layout(self.__layout.get_active()):
            self.__layout.set_active(self.radialnet.get_layout())

        else:
            self.__check_layout()


class ControlRingGap(BWVBox):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWVBox.__init__(self)

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__radius = ControlVariable(_('Ring gap'),
                                        self.radialnet.get_ring_gap,
                                        self.radialnet.set_ring_gap)

        self.__label = gtk.Label(_('Lower ring gap'))
        self.__label.set_alignment(0.0, 0.5)
        self.__adjustment = gtk.Adjustment(self.radialnet.get_min_ring_gap(),
                                           0,
                                           50,
                                           1)
        self.__spin = gtk.SpinButton(self.__adjustment)
        self.__spin.connect('value_changed', self.__change_lower)

        self.__lower_hbox = BWHBox()
        self.__lower_hbox.bw_pack_start_expand_fill(self.__label)
        self.__lower_hbox.bw_pack_start_noexpand_nofill(self.__spin)

        self.bw_pack_start_noexpand_nofill(self.__radius)
        self.bw_pack_start_noexpand_nofill(self.__lower_hbox)

    def __change_lower(self, widget):
        """
        """
        if not self.radialnet.set_min_ring_gap(self.__adjustment.get_value()):
            self.__adjustment.set_value(self.radialnet.get_min_ring_gap())


class ControlOptions(BWScrolledWindow):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWScrolledWindow.__init__(self)

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.set_shadow_type(gtk.SHADOW_NONE)

        self.radialnet = radialnet

        self.enable_labels = True

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__liststore = gtk.ListStore(gobject.TYPE_BOOLEAN,
                                         gobject.TYPE_STRING)

        self.__liststore.append([None, OPTIONS[0]])
        self.__liststore.append([None, OPTIONS[1]])
        self.__liststore.append([None, OPTIONS[2]])
        self.__liststore.append([None, OPTIONS[3]])
        self.__liststore.append([None, OPTIONS[4]])
        self.__liststore.append([None, OPTIONS[5]])
        self.__liststore.append([None, OPTIONS[6]])

        self.__cell_toggle = gtk.CellRendererToggle()
        self.__cell_toggle.set_property('activatable', True)
        self.__cell_toggle.connect('toggled',
                                   self.__change_option,
                                   self.__liststore)

        self.__column_toggle = gtk.TreeViewColumn('', self.__cell_toggle)
        self.__column_toggle.add_attribute(self.__cell_toggle, 'active', 0)
        self.__column_toggle.set_cell_data_func(self.__cell_toggle, self.__cell_toggle_data_method)

        self.__cell_text = gtk.CellRendererText()

        self.__column_text = gtk.TreeViewColumn(None,
                                                self.__cell_text,
                                                text=1)
        self.__column_text.set_cell_data_func(self.__cell_text, self.__cell_text_data_method)

        self.__treeview = gtk.TreeView(self.__liststore)
        self.__treeview.set_enable_search(True)
        self.__treeview.set_search_column(1)
        self.__treeview.set_headers_visible(False)
        self.__treeview.append_column(self.__column_toggle)
        self.__treeview.append_column(self.__column_text)

        self.add_with_viewport(self.__treeview)

        gobject.timeout_add(REFRESH_RATE, self.__update_options)

    def __cell_toggle_data_method(self, column, cell, model, it):
        if not self.enable_labels and model.get_value(it, 1) == 'hostname':
            cell.set_property('activatable', False)
        else:
            cell.set_property('activatable', True)

    def __cell_text_data_method(self, column, cell, model, it):
        if not self.enable_labels and model.get_value(it, 1) == 'hostname':
            cell.set_property('strikethrough', True)
        else:
            cell.set_property('strikethrough', False)

    def __update_options(self):
        """
        """
        model = self.__liststore

        model[OPTIONS.index('address')][0] = self.radialnet.get_show_address()
        model[OPTIONS.index('hostname')][0] = self.enable_labels and \
                self.radialnet.get_show_hostname()
        model[OPTIONS.index('icon')][0] = self.radialnet.get_show_icon()
        model[OPTIONS.index('latency')][0] = self.radialnet.get_show_latency()
        model[OPTIONS.index('ring')][0] = self.radialnet.get_show_ring()
        model[OPTIONS.index('region')][0] = self.radialnet.get_show_region()
        model[OPTIONS.index('slow in/out')][0] = \
                self.radialnet.get_slow_inout()

        return True

    def __change_option(self, cell, option, model):
        """
        """
        option = int(option)
        model[option][0] = not model[option][0]

        if OPTIONS[option] == 'address':
            self.radialnet.set_show_address(model[option][0])
            if model[option][0]:
                model[OPTIONS.index('hostname')][0] = self.radialnet.get_show_hostname()
            else:
                model[OPTIONS.index('hostname')][0] = False
            self.enable_labels = model[option][0]

        elif OPTIONS[option] == 'hostname':
            self.radialnet.set_show_hostname(model[option][0])

        elif OPTIONS[option] == 'icon':
            self.radialnet.set_show_icon(model[option][0])

        elif OPTIONS[option] == 'latency':
            self.radialnet.set_show_latency(model[option][0])

        elif OPTIONS[option] == 'ring':
            self.radialnet.set_show_ring(model[option][0])

        elif OPTIONS[option] == 'region':
            self.radialnet.set_show_region(model[option][0])

        elif OPTIONS[option] == 'slow in/out':
            self.radialnet.set_slow_inout(model[option][0])


class ControlView(BWExpander):
    """
    """
    def __init__(self, radialnet):
        """
        """
        BWExpander.__init__(self, _('View'))
        self.set_expanded(True)

        self.radialnet = radialnet

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__vbox = BWVBox(spacing=0)

        self.__zoom = ControlVariable(_('Zoom'),
                                      self.radialnet.get_zoom,
                                      self.radialnet.set_zoom)

        self.__ring_gap = ControlRingGap(self.radialnet)
        self.__navigation = ControlNavigation(self.radialnet)

        self.__options = ControlOptions(self.radialnet)
        self.__options.set_border_width(0)

        self.__vbox.bw_pack_start_expand_nofill(self.__options)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__navigation)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__zoom)
        self.__vbox.bw_pack_start_noexpand_nofill(self.__ring_gap)

        self.bw_add(self.__vbox)


class ControlNavigation(gtk.DrawingArea):
    """
    """
    def __init__(self, radialnet):
        """
        """
        gtk.DrawingArea.__init__(self)

        self.radialnet = radialnet

        self.__rotate_node = PolarCoordinate()
        self.__rotate_node.set_coordinate(40, 90)
        self.__center_of_widget = (50, 50)
        self.__moving = None
        self.__centering = False
        self.__rotating = False
        self.__move_pass = 100

        self.__move_position = (0, 0)
        self.__move_addition = [(-1, 0),
                                (-1, -1),
                                (0, -1),
                                (1, -1),
                                (1, 0),
                                (1, 1),
                                (0, 1),
                                (-1, 1)]

        self.__move_factor = 1
        self.__move_factor_limit = 20

        self.__rotate_radius = 6
        self.__move_radius = 6

        self.__rotate_clicked = False
        self.__move_clicked = None

        self.connect('expose_event', self.expose)
        self.connect('button_press_event', self.button_press)
        self.connect('button_release_event', self.button_release)
        self.connect('motion_notify_event', self.motion_notify)
        self.connect('enter_notify_event', self.enter_notify)
        self.connect('leave_notify_event', self.leave_notify)
        self.connect('key_press_event', self.key_press)
        self.connect('key_release_event', self.key_release)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.ENTER_NOTIFY |
                        gtk.gdk.LEAVE_NOTIFY |
                        gtk.gdk.MOTION_NOTIFY |
                        gtk.gdk.NOTHING |
                        gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

        self.__rotate_node.set_coordinate(40, self.radialnet.get_rotation())

    def key_press(self, widget, event):
        """
        """
        # key = gtk.gdk.keyval_name(event.keyval)

        self.queue_draw()

        return True

    def key_release(self, widget, event):
        """
        """
        # key = gtk.gdk.keyval_name(event.keyval)

        self.queue_draw()

        return True

    def enter_notify(self, widget, event):
        """
        """
        return False

    def leave_notify(self, widget, event):
        """
        """
        self.queue_draw()

        return False

    def button_press(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        pointer = self.get_pointer()

        direction = False

        if self.__rotate_is_clicked(pointer):

            event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.__rotating = True

        direction = self.__move_is_clicked(pointer)

        if direction is not None and self.__moving is None:

            event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.__moving = direction
            self.__move_in_direction(direction)

        if self.__center_is_clicked(pointer):

            event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            self.__centering = True
            self.__move_position = (0, 0)
            self.radialnet.set_translation(self.__move_position)

        self.queue_draw()

        return False

    def button_release(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        self.__moving = None        # stop moving
        self.__centering = False
        self.__rotating = False     # stop rotate
        self.__move_factor = 1

        event.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

        self.queue_draw()

        return False

    def motion_notify(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        xc, yc = self.__center_of_widget
        x, y = self.get_pointer()

        status = not self.radialnet.is_in_animation()
        status = status and not self.radialnet.is_empty()

        if self.__rotating and status:

            r, t = self.__rotate_node.get_coordinate()
            t = math.degrees(math.atan2(yc - y, x - xc))

            if t < 0:
                t = 360 + t

            self.radialnet.set_rotation(t)
            self.__rotate_node.set_coordinate(r, t)

            self.queue_draw()

        return False

    def expose(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        self.set_size_request(120, 130)

        self.context = widget.window.cairo_create()
        self.__draw()

        return False

    def __draw_rotate_control(self):
        """
        """
        xc, yc = self.__center_of_widget
        r, t = self.__rotate_node.get_coordinate()
        x, y = self.__rotate_node.to_cartesian()

        # draw text
        self.context.set_font_size(10)
        self.context.move_to(xc - 49, yc - 48)
        self.context.show_text(_("Navigation"))

        width = self.context.text_extents(str(int(t)))[2]
        self.context.move_to(xc + 49 - width - 2, yc - 48)
        self.context.show_text(str(round(t, 1)))
        self.context.set_line_width(1)
        self.context.stroke()

        # draw arc
        self.context.set_dash([1, 2])
        self.context.arc(xc, yc, 40, 0, 2 * math.pi)
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.set_line_width(1)
        self.context.stroke()

        # draw node
        self.context.set_dash([1, 0])
        self.context.arc(xc + x, yc - y, self.__rotate_radius, 0, 2 * math.pi)

        if self.__rotating:
            self.context.set_source_rgb(0.0, 0.0, 0.0)

        else:
            self.context.set_source_rgb(1.0, 1.0, 1.0)

        self.context.fill_preserve()
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.set_line_width(1)
        self.context.stroke()

        return False

    def __draw_move_control(self):
        """
        """
        xc, yc = self.__center_of_widget
        pc = PolarCoordinate()

        self.context.set_dash([1, 1])
        self.context.arc(xc, yc, 23, 0, 2 * math.pi)
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.set_line_width(1)
        self.context.stroke()

        for i in range(8):

            pc.set_coordinate(23, 45 * i)
            x, y = pc.to_cartesian()

            self.context.set_dash([1, 1])
            self.context.move_to(xc, yc)
            self.context.line_to(xc + x, yc - y)
            self.context.stroke()

            self.context.set_dash([1, 0])
            self.context.arc(
                    xc + x, yc - y, self.__move_radius, 0, 2 * math.pi)

            if i == self.__moving:
                self.context.set_source_rgb(0.0, 0.0, 0.0)
            else:
                self.context.set_source_rgb(1.0, 1.0, 1.0)
            self.context.fill_preserve()
            self.context.set_source_rgb(0.0, 0.0, 0.0)
            self.context.set_line_width(1)
            self.context.stroke()

        self.context.arc(xc, yc, 6, 0, 2 * math.pi)

        if self.__centering:
            self.context.set_source_rgb(0.0, 0.0, 0.0)
        else:
            self.context.set_source_rgb(1.0, 1.0, 1.0)
        self.context.fill_preserve()
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.set_line_width(1)
        self.context.stroke()

        return False

    def __draw(self):
        """
        Drawing method
        """
        # Getting allocation reference
        allocation = self.get_allocation()

        self.__center_of_widget = (allocation.width / 2,
                                   allocation.height / 2)

        self.__draw_rotate_control()
        self.__draw_move_control()

        return False

    def __move_in_direction(self, direction):
        """
        """
        if self.__moving is not None:

            bx, by = self.__move_position
            ax, ay = self.__move_addition[direction]

            self.__move_position = (bx + self.__move_factor * ax,
                                    by + self.__move_factor * ay)
            self.radialnet.set_translation(self.__move_position)

            if self.__move_factor < self.__move_factor_limit:
                self.__move_factor += 1

            gobject.timeout_add(self.__move_pass,
                                self.__move_in_direction,
                                direction)

        return False

    def __rotate_is_clicked(self, pointer):
        """
        """
        xn, yn = self.__rotate_node.to_cartesian()
        xc, yc = self.__center_of_widget

        center = (xc + xn, yc - yn)
        return geometry.is_in_circle(pointer, self.__rotate_radius, center)

    def __center_is_clicked(self, pointer):
        """
        """
        return geometry.is_in_circle(pointer, self.__move_radius,
                self.__center_of_widget)

    def __move_is_clicked(self, pointer):
        """
        """
        xc, yc = self.__center_of_widget
        pc = PolarCoordinate()

        for i in range(8):

            pc.set_coordinate(23, 45 * i)
            x, y = pc.to_cartesian()

            center = (xc + x, yc - y)
            if geometry.is_in_circle(pointer, self.__move_radius, center):
                return i

        return None
