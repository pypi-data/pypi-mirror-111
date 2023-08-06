.. _overview:

Overview of SwitchRound
=======================

Quickstart: Importing and using SwitchRound
-------------------------------------------

Here is one way of importing the `SwitchRound` class so you can use it as
the name :data:`Switch`:

.. code-block:: python

    from displayio_switchround import SwitchRound as Switch

Now you can create a switch at pixel position x=20, y=30 using:

.. code-block:: python

    my_switch = Switch(20, 30) # create the switch at x=20, y=30

Once you setup your display, you can now add :data:`my_switch` to your display using:

.. code-block:: python

    display.show(my_switch)  # add the group to the display

If you want to have multiple display elements, you can create a group and then
append the switch and the other elements to the group. Then, you can add the full
group to the display as in this example:

.. code-block:: python

    my_switch = Switch(20, 30)  # create the switch at x=20, y=30
    my_group = displayio.Group()  # make a group
    my_group.append(my_switch)  # Add my_switch to the group

    #
    # Append other display elements to the group
    #

    display.show(my_group)  # add the group to the display

For a full example, including how to respond to screen touches, check out the
following examples in the `Adafruit_CircuitPython_DisplayIO_Layout
<https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_Layout>`_ library:

    - `examples/displayio_layout_switch_simpletest.py
      <https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_Layout/blob/main/examples/displayio_layout_switch_simpletest.py>`_
    - `examples/displayio_layout_switch_multiple.py
      <https://github.com/adafruit/Adafruit_CircuitPython_DisplayIO_Layout/blob/main/examples/displayio_layout_switch_multiple.py>`_

Summary: SwitchRound Features and input variables
-------------------------------------------------

The `SwitchRound` widget has numerous options for controlling its position, visible appearance,
orientation, animation speed and value through a collection of input variables:

    - **position**:
        :attr:`~displayio_switchround.SwitchRound.x` and
        :attr:`~displayio_switchround.SwitchRound.y` or
        :attr:`~displayio_switchround.SwitchRound.anchor_point` and
        :attr:`~displayio_switchround.SwitchRound.anchored_position`


    - **size**:
        :attr:`~displayio_switchround.SwitchRound.width` and
        :attr:`~displayio_switchround.SwitchRound.height`

        It is recommended to leave :data:`width = None` to use the preferred aspect
        ratio.

    - **orientation and movement direction (on vs. off)**:
        :attr:`~displayio_switchround.SwitchRound.horizontal` and
        :attr:`~displayio_switchround.SwitchRound.flip`

    - **switch color**:
        :attr:`~displayio_switchround.SwitchRound.fill_color_off`,
        :attr:`~displayio_switchround.SwitchRound.fill_color_on`,
        :attr:`~displayio_switchround.SwitchRound.outline_color_off` and
        :attr:`~displayio_switchround.SwitchRound.outline_color_on`

    - **background color**:
        :attr:`~displayio_switchround.SwitchRound.background_color_off`,
        :attr:`~displayio_switchround.SwitchRound.background_color_on`,
        :attr:`~displayio_switchround.SwitchRound.background_outline_color_off` and
        :attr:`~displayio_switchround.SwitchRound.background_outline_color_on`

    - **linewidths**:
        :attr:`~displayio_switchround.SwitchRound.switch_stroke` and
        :attr:`~displayio_switchround.SwitchRound.text_stroke`

    - **0/1 display**:
        :attr:`~displayio_switchround.SwitchRound.display_button_text`

        Set to `True` if you want the 0/1 shapes
        to show on the switch

    - **animation**:
        :attr:`~displayio_switchround.SwitchRound.animation_time`

        Set the duration (in seconds) it will take to transition the switch, use
        :data:`0` if you want it to snap into position immediately. The default value
        of :data:`0.2` seconds is a good starting point, and larger values for bigger
        switches.

    - **value**:
        :attr:`~displayio_switchround.SwitchRound.value`

        Set to the initial value (`True` or `False`)

    - **touch boundaries**:
        :attr:`~displayio_switchround.SwitchRound.touch_padding`

        This defines the number of additional pixels surrounding the switch that should
        respond to a touch.  (Note: The :attr:`touch_padding` variable updates the
        :attr:`touch_boundary` Control class variable.  The definition of the
        :attr:`touch_boundary` is used to determine the region on the Widget that returns
        `True` in the :meth:`~displayio_switchround.SwitchRound.contains` method.)

Description of features
-----------------------

The `SwitchRound` widget is a sliding switch that changes state whenever it is touched.
The color gradually changes from the off-state color scheme to the on-state color
scheme as the switch transfers from off to the on position. The switch has an optional
display of "0" and "1" on the sliding switch. The switch can be oriented using the
:attr:`~displayio_switchround.SwitchRound.horizontal` input variable, and the sliding
direction can be changed using the :attr:`~displayio_switchround.SwitchRound.flip`
input variable.

Regarding switch sizing, it is recommended to set the height dimension but to leave the
:data:`width = None`. Setting :data:`width = None` will allow the width to resize to
maintain a recommended aspect ratio of width/height. Alternately, the switch can be
resized using the :meth:`~displayio_switchround.SwitchRound.resize` method, and it will
adjust the width and height to the maximum size that will fit inside the requested
width and height dimensions, while keeping the preferred aspect ratio. To make the
switch easier to be selected, additional padding around the switch can be defined using
the :attr:`~displayio_switchround.SwitchRound.touch_padding` input variable to increase
the touch-responsive area. The duration of animation between on/off can be set using
the :attr:`~displayio_switchround.SwitchRound.animation_time` input variable.

Internal details: How the SwitchRound widget works
--------------------------------------------------

The `SwitchRound` widget is a graphical element that responds to touch elements to
provide sliding switch on/off behavior. Whenever touched, the switch toggles to its
alternate value. The following sections describe the construction of the `SwitchRound`
widget, in the hopes that it will serve as a first example of the key properties and
responses for widgets.

.. inheritance-diagram:: displayio_switchround

|

The `SwitchRound` widget inherits from two classes, it is a subclass of
:class:`~adafruit_displayio_layout.widgets.widget.Widget`, which itself is a subclass
of `displayio.Group`, and a subclass of
:class:`~adafruit_displayio_layout.widgets.control.Control`. The
:class:`~adafruit_displayio_layout.widgets.widget.Widget` class helps define the
positioning and sizing of the switch, while th
:class:`~adafruit_displayio_layout.widgets.control.Control` class helps define the
touch-response behavior.

The following sections describe the structure and inner workings of `SwitchRound`.

Group structure: Display elements that make up SwitchRound
----------------------------------------------------------

The :class:`~adafruit_displayio_layout.widgets.widget.Widget`
class is a subclass of `displayio.Group`, thus we can append graphical
elements to the Widget for displaying on the screen. The switch consists of the
following graphical elements:

    0. switch_roundrect: The switch background
    1. switch_circle: The switch button that slides back and forth
    2. text_0 [Optional]: The "0" circle shape on the switch button
    3. text_1 [Optional]: The "1" rectangle shape on the switch button

The optional text items can be displayed or hidden using the
:attr:`~displayio_switchround.SwitchRound.display_button_text` input variable.

Coordinate systems and use of anchor_point and anchored_position
----------------------------------------------------------------

See the :class:`~adafruit_displayio_layout.widgets.widget.Widget` class definition for
clarification on the methods for positioning the switch, including the difference in
the display coordinate system and the Widget's local coordinate system.

The Widget construction sequence
--------------------------------

Here is the set of steps used to define this sliding switch widget.

    1. Initialize the stationary display items
    2. Initialize the moving display elements
    3. Store initial position of the moving display elements
    4. Define "keyframes" to determine the translation vector
    5. Define the :meth:`SwitchRound._draw_position` method between 0.0 to 1.0 (and
       slightly beyond)
    6. Select the motion "easing" function
    7. **Extra**. Go check out the :meth:`SwitchRound._animate_switch` method

First, the stationary background rounded rectangle (RoundRect is created). Second, the
moving display elements are created, the circle for the switch, the circle for the text
"0" and the rectangle for the text "1". Note that either the "0" or "1" is set as
hidden, depending upon the switch value. Third, we store away the initial position of
the three moving elements, these initial values will be used in the functions that move
these display elements. Next, we define the motion of the moving element, by setting
the :data:`self._x_motion` and :data:`self._y_motion` values that depending upon the
:attr:`~SwitchRound.horizontal` and :attr:`~SwitchRound.flip` variables. These motion
variables set the two "keyframes" for the moving elements, basically the endpoints of
the switch motion. (Note: other widgets may need an :data:`_angle_motion` variable if
they require some form of rotation.) Next, we define the
:meth:`SwitchRound._draw_function` method. This method takes an input between 0.0 and
1.0 and adjusts the position relative to the motion variables, where 0.0 is the initial
position and 1.0 represents the final position (as defined by the :data:`_x_motion` and
:data:`_y_motion` values). In the case of the sliding switch, we also use this
:attr:`SwitchRound.position` value (0.0 to 1.0) to gradually grade the color of the
components between their "on" and "off" colors.

Making it move
--------------

Everything above has set the ground rules for motion, but doesn't cause it to move.
However, you have set almost all the pieces in place to respond to requests to change
the position. All that is left is the **Extra** method that performs the animation,
called :meth:`SwitchRound._animate_switch`. The :meth:`SwitchRound._animate_switch`
method is triggered by a touch event through the
:meth:`~adafruit_displayio_layout.widgets.control.Control.selected` Control class
method. Once triggered, this method
checks how much time has elapsed. Based on the elapsed time and the
:attr:`SwitchRound.animation_time` input variable, the
:meth:`SwitchRound._animate_switch` method calculates the :attr:`SwitchRound.position`
where the switch should be. Then, it takes this :attr:`SwitchRound.position` to call
the :meth:`SwitchRound._draw_position` method that will update the display elements
based on the requested position.

But there's even one more trick to the animation. The
:meth:`SwitchRound._animate_switch` calculates the target position based on a linear
relationship between the time and the position. However, to give the animation a better
"feel", it is desirable to tweak the motion function depending upon how this widget
should behave or what suits your fancy. To do this we can use an *"easing"* function.
In short, this adjusts the constant speed (linear) movement to a variable speed during
the movement. Said another way, it changes the position versus time function according
to a specific waveform equation. There are a lot of different "easing" functions that
folks have used or you can make up your own. Some common easing functions are provided
in the :mod:`adafruit_displayio_layout.widgets.easing` module. You can change the
easing function based on changing which function is imported at the top of this file.
You can see where the position is tweaked by the easing function in the line in the
:meth:`SwitchRound._animate_switch` method:

.. code-block:: python

    self._draw_position(easing(position))  # update the switch position

Go play around with the different easing functions and observe how the motion
behavior changes.  You can use these functions in multiple dimensions to get all
varieties of behavior that you can take advantage of.  The website
`easings.net <https://easings.net>`_ can help you
visualize some of the behavior of the easing functions.

.. note:: Some of the "springy" easing functions require position values
        slightly below 0.0 and slightly above 1.0, so if you want to use these, be sure
        to check that your :meth:`_draw_position` method behaves itself for that range
        of position inputs.

Orientation and a peculiarity of width and height definitions for SwitchRound
-----------------------------------------------------------------------------

In setting the switch sizing, use height and width to set the narrow and wide dimension
of the switch. To try and reduce confusion, the orientation is modified after the
height and width are selected. That is, if the switch is set to vertical, the height
and still mean the "narrow" and the width will still mean the dimensions
in the direction of the sliding.

If you need the switch to fit within a specific bounding box, it's preferred to use
the :meth:`~displayio_switchround.SwitchRound.resize` function. This will put the switch (in whatever
orientation) at the maximum size where it can fit within the bounding box that you
specified. The Switch aspect ratio will remain at the "preferred" aspect ratio of 2:1
(width:height) after the resizing.

Setting the touch response boundary
-----------------------------------

The touch response area is defined by the Control class variable called
:data:`touch_boundary`. In the case of the `SwitchRound` widget, we provide an
:attr:`SwitchRound.touch_padding` input variable. The use of
:attr:`SwitchRound.touch_padding` defines an additional number of pixels surrounding
the display elements that respond to touch events. To achieve this additional space,
the :data:`touch_boundary` increases in size in all dimensions by the number of pixels
specified in the :attr:`SwitchRound.touch_padding` parameter.

The :data:`touch_boundary` is used in the Control function
:meth:`~displayio_switchround.SwitchRound.contains` that checks whether any
touch_points are within the boundary. Please pay particular attention to the
`SwitchRound` :meth:`~displayio_switchround.SwitchRound.contains` method, since it
calls the :meth:`~adafruit_displayio_layout.widgets.control.Control.contains`
superclass method with the touch_point value adjusted for the switch's
:attr:`~displayio_switchround.SwitchRound.x` and
:attr:`~displayio_switchround.SwitchRound.y` values. This offset adjustment is
required since the :meth:`~adafruit_displayio_layout.widgets.control.Control.contains`
function operates only on the widget's local coordinate system. It's good to keep in
mind which coordinate system you are working in, to ensure your code responds to the
right inputs!

Summary
-------

The `SwitchRound` widget is an example to explain the use of the
:class:`~adafruit_displayio_layout.widgets.widget.Widget` and
:class:`~adafruit_displayio_layout.widgets.control.Control` class methods. The
:class:`~adafruit_displayio_layout.widgets.widget.Widget` class handles the overall
sizing and positioning function and is the group that holds all the graphical elements.
The :class:`~adafruit_displayio_layout.widgets.control.Control` class is used to define
the response of the widget to touch events (or could be generalized to other inputs).
Anything that only displays (such as a graph or an indicator light) won't need to
inherit the :class:`~adafruit_displayio_layout.widgets.control.Control` class. But
anything that responds to touch inputs should inherit the
:class:`~adafruit_displayio_layout.widgets.control.Control` class to define the
:data:`touch_boundary` and the touch response functions.

I hope this `SwitchRound` widget will help turn on some new ideas and highlight some
of the new capabilities of the :class:`~adafruit_displayio_layout.widgets.widget.Widget`
and :class:`~adafruit_displayio_layout.widgets.control.Control` classes.  Now go see
what else you can create and extend from here!

A Final Word
------------

The design of the Widget and Control classes are open for inputs.  If you think any
additions or changes are useful, add it and please submit a pull request so others can
use it too! Also, keep in mind you don't even need to follow these classes to get the
job done. The Widget and Class definitions are designed to give guidance about one way
to make things work, and to try to share some code. If it's standing in your way, do
something else!  If you want to use the ``grid_layout`` or other layout tools in this
library, you only *really* need to have methods for positioning and resizing.

.. note:: **Never let any of these class definitions hold you back, let your imagination
    run wild and make some cool widgets!**
