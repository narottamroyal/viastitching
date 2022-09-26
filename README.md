# Via Stitching

Via Stitching action-plugin for use with KiCad 6.0+.

Fill a selected copper area with a pattern of vias.

## When to use this tool

Whenever you need to fill a copper area with vias to improve thermal or current conduction this tool is the answer (yet not the best one probably). The plugin is based on pre-existing areas so you have to define and select one before invoking the plugin.

## How it works

The workflow is pretty simple: select the area you want to fill, click on ```Tools->External Plugins->ViaStitching``` or click on ![AddNet icon](viastitching.png?raw=true) toolbar icon, and a dialog like the one below should appear:

![AddNet dialog](pictures/viastitching_dialog.PNG?raw=true "ViaStitching dialog")

The vias this plugin creates need to be assigned to a net; usually this is the net of the target area, so the plugin select this net for you by default (of course you're free to select another net if desired).
The plugin dialog also lets you specify the via size and drill size. The current via dimensions are used by default; you can change them but beware these values may conflict with DRC rules.
You can also customize the vertical and horizontal spacing between vias, and the edge clearance (a value of 0 will disable clearance checking).
When you're satisfied with the settings, just to press __Ok__ and the vias will be generated (assuming __Fill__ was selected).
If everything goes well, you'll get something like this:

![viastitching result](pictures/viastitching_result.PNG?raw=true "ViaStitching result")

After stitching is always a good practice to perform a DRC.

As you can see some implanted vias may still overlap with some other PCB elements (tracks, ~~zone, pads, vias~~ etc) at this development stage the removal of conflicting vias is up to the user with future releases the implant process will prevent vias to overlap with other elements.

The default action of the dialog is the __Fill__ action (as you can notice from the radio-button on the bottom) but this plugin is not limited to this function only. __Clear__ action works the in the opposite way: it removes from selected area any vias matching settings (i.e. same net, same size, same drill specified in dialog fields). Beware: __Clear__ will not distinguish vias implanted by __Fill__ from user ones until you check the specific checkbox, and will remove all of them if they match the values entered. If you check __clear only plugin placed vias__ widget the plugin will inspect vias grouped on a specific group and remove only those matching: this can be used as an __Undo__ feature.

## TODO

Some features still to code:
- [x] Match user units (mm/inches).
- [x] Add clear area function.
- [ ] Draw a better UI (if anyone is willing to contribute please read the following section).
- [x] Collision between new vias and underlying objects: 
   - [x] tracks, 
   - [x] zones, 
   - [x] pads,
   - [x] modules,
   - [x] vias.
- [ ] Different fillup patterns/modes (bounding box, centered spiral).
- [x] Avoid placing vias near area edges (define clearance).
- [ ] History management (board commit).
- [ ] Localization.
- [ ] Any request?

## Coding notes

If you are willing to modify the GUI (you're welcome) through __wxFormBuilder__ (```viastitching.fbp``` file) remember to modify this line (around line 25 ```viastitching_gui.py```):
```
self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
```
In this way:
```
if sys.version_info[0] == 2:
 self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
else:
 self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
```
This modification allows the code to work with __Python 2__ as well as __Python 3__, please note that you need to ```import sys```. Special thanks to *NilujePerchut* for this hint.

## kicad-action-scripts - ViaStitching plugin similarity

Yes, my plugin is pretty similar to this plugin, but I'm using a radically different approach in coding. At the time I wrote the first release of my plugin unluckly __jsreynaud__'s plugin wasn't working but I bet he will fix it.

## References

Some useful references that helped me coding this plugin:
1. https://sourceforge.net/projects/wxformbuilder/
2. https://wxpython.org/
3. http://docs.kicad-pcb.org/doxygen-python/namespacepcbnew.html
4. https://forum.kicad.info/c/external-plugins
5. https://github.com/KiCad/kicad-source-mirror/blob/master/Documentation/development/pcbnew-plugins.md
6. https://kicad.mmccoo.com/
7. http://docs.kicad-pcb.org/5.1.4/en/pcbnew/pcbnew.html#kicad_scripting_reference


Tool I got inspired by:
- Altium Via Stitching feature!
- https://github.com/jsreynaud/kicad-action-scripts

## Greetings

I hope someone finds my work useful or at least provides *inspiration* to create something else/better.
I would like to thank everyone who has shared their knowledge of Python and KiCad with me: Thanks!

#

Live long and prosper!

That's all folks.

By[t]e{s}
 Weirdgyn
