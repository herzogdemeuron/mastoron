Visualize
=========

.. _color-schemes:

Color Schemes
+++++++++++++

.. _apply-color-scheme:

Apply Color Scheme
------------------

Applies a color scheme for a parameter of your choice to all selected objects. A set of easily distinguishable colors is applied by default.

Edit Color Scheme
------------------

Lets you edit the colors for a color scheme. After saving your changes to the color scheme, you have to update all the element overrides using any of the :ref:`update` buttons.

Export Color Scheme
-------------------

Exports a color scheme of your choice to a .json file. You can import this color scheme into another project. If you want to change the parameter of a color scheme but keep the colors for the values you can manually edit the exported file and re-import the color scheme.

Import Color Scheme
-------------------

Imports a color scheme from a .json file. This is handy if you want to fetch the colors from another file or project.


Charts
++++++

Charts require at least on color scheme to be already defined. 
To make a colors scheme, use the :ref:`apply-color-scheme` button.

Bar Chart
---------

Create a data visualization in for of a bar chart for the selected objects.

Color Scheme
    Select a color scheme to define the bars of your chart.

Values  
    Select the parameter for the length of the bars.


.. _update:

Update
++++++

Update Colors in Current View
-----------------------------

Update Colors in Selected Views
-------------------------------


Clear Colors
------------

Clear all color overrides for a color scheme in current view. This button currently has auto-purging buit-in, meaning that if the cleared view containing a color scheme was cleared, the color scheme will be deleted.