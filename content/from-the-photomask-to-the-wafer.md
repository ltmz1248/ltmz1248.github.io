---
title: "From the Photomask to the Wafer"
description: "An illustrated reading of Lecture 38: how a mask becomes a physical pattern through imaging, resist chemistry, development, and etching."
pubDate: "2026-09-20"
tags: ["Lithography", "OPC", "ILT"]
---

# From the Photomask to the Wafer

Lithography begins with a simple intention: reproduce a pattern on a wafer. What makes the task difficult is doing it at very small dimensions, repeatedly, and at an acceptable cost. Chris Mack defines it as a printing technique based on the production of a three-dimensional relief image on a substrate (writing on stones). His lecture keeps returning to the manufacturing constraint: Lithography improvements must enable the printing of smaller features without significantly increasing the cost of making the chip. That connection between dimensions and production is a useful place to begin thinking about OPC and ILT.

It helps to be precise about the pattern we want. Mack's textbook describes the ideal directly: In general, the ideal photoresist image has the exact shape of the designed or intended pattern in the plane of the substrate, with vertical walls through the thickness of the resist. He then makes the requirement physical: Thus, the final resist pattern should be binary: parts of the substrate are covered with resist while other parts are completely uncovered. The resist has to protect some regions and leave others accessible to the next process. Its shape through the film matters as much as its outline.

The lecture brings together four ingredients: a master pattern to be reproduced called a photomask, a photosensitive film called a photoresist, a special camera (called a stepper or a scanner) that projects an image of the photomask into the photoresist, and a tool for processing the photoresist (coating, baking, developing) called a track. The sequence below gives those ingredients a place in the process. Coating and baking prepare the film; exposure writes the image; another bake and development turn it into a relief pattern that can be measured.

![The original Lecture 38 diagram showing coating, prebake, projection exposure, post-exposure bake, development, and metrology.](assets/lecture38/lithography-sequence.png)

*Figure 1. The complete lithography sequence.*

Even before exposure, the film needs careful control. A thin, uniform coating of photoresist at a specific, well-controlled thickness is accomplished by the seemingly simple process of spin coating. The word seemingly is well chosen: the next step is already changing that film. The main reason for reducing the solvent content is to stabilize the resist film. At room temperature, an unbaked photoresist film will lose solvent by evaporation, thus changing the properties of the film with time. The post-apply bake therefore prepares a reproducible starting point for imaging. For chemically amplified resists, residual solvent can significantly influence diffusion and reaction properties during the post-exposure bake, necessitating careful control over the post-apply bake process.

![Original comparison of contact printing, proximity printing, and projection printing.](assets/lecture38/printing-methods.gif)

*Figure 2. Contact, proximity, and projection printing.*

The mask then enters an optical system. Projection lithography derives its name from the fact that an image of the mask is projected onto the wafer. Mack describes a diffraction-limited system this way: Such an optical system is said to be diffraction-limited, since it is diffraction effects and not lens aberrations which, for the most part, determine the shape of the image. A good lens does not make the printed result a perfect geometric copy. The next qualification is equally useful: Resolution, the smallest feature that can be printed with adequate control, has two basic limits: the smallest image that can be projected onto the wafer, and the resolving capability of the photoresist to make use of that image.

Before this image can be used, it must be placed on a wafer that already carries patterns from earlier steps. Before the exposure of the photoresist with an image of the mask can begin, this image must be aligned with the previously defined patterns on the wafer. Mack continues: This alignment process, and the resulting overlay of the two or more lithographic patterns, is critical since tighter overlay control means circuit features can be packed closer together. Focus belongs to this preparation too: Along with alignment, wafer focus is measured at several points so that each exposure field is leveled and brought into proper focus. The printed pattern has to work within the structure being built, layer after layer.

The image also has a depth. As Mack explains on his website, light reflected from the substrate interferes with the incoming light, producing alternating high and low intensity through the resist. The ridged sidewalls in the original micrograph below make that effect visible. The same interference makes linewidth vary with resist thickness, giving the swing curves discussed in the reading. An absorbing bottom antireflective coating reduces the reflected light. The film and substrate beneath the mask help determine what gets printed.

![Original micrograph showing standing-wave ridges in the sidewalls of a developed photoresist pattern.](assets/lecture38/standing-waves.gif)

*Figure 3. Standing-wave ridges in a developed photoresist pattern.*

Exposure is followed by another bake, whose role depends on the resist. For a conventional resist, the main importance of the PEB is diffusion to remove standing waves. For another class of photoresists, called chemically amplified resists, the PEB is an essential part of the chemical reactions that create a solubility differential between exposed and unexposed parts of the resist. For the latter, exposure generates acid. During the post-exposure bake, this photogenerated acid catalyzes a reaction that changes the solubility of the polymer resin in the resist. The image is still being formed after the light has been switched off.

![Mack's original three simulated resist profiles at PEB diffusion lengths of 20, 40, and 60 nm, including the original caption.](assets/lecture38/peb-profiles.png)

*Figure 4. Diffusion smooths the standing-wave ridges in these conventional-resist simulations. The original caption is retained.*

Development makes the relief image visible, but it also helps set its dimensions. The characteristics of the resist-developer interactions determine to a large extent the shape of the photoresist profile and, more importantly, the linewidth control. This explains why the process diagram ends with metrology rather than simply stopping at exposure. Mack describes the practical check: Critical features and test patterns are measured to determine their dimensions (called a critical dimension, CD) and the overlay of the patterns with respect to previous lithographically defined layers. The result must have the right dimensions and occupy the right position on the wafer.

![Original Lecture 38 slide illustrating the polysilicon subtractive-patterning sequence and the mask, resist, film, and wafer.](assets/lecture38/subtractive-patterning.png)

*Figure 5. The polysilicon pattern-transfer example from Lecture 38.*

The final destination is the material underneath. Lecture 38 gives the example plainly: Expose and develop photoresist to create pattern, then etch pattern into polysilicon using resist as mask, and finally strip away the resist. The temporary resist image has done its job when the intended structure remains in the deposited film. That is the thread I would carry into further reading on OPC and ILT: follow the pattern from the mask, through the optical image and resist chemistry, to the feature that can actually be measured and transferred.

---

**Sources and image credits.** This article draws on Chris A. Mack's [Lecture 38: Lithography Introduction](https://www.youtube.com/watch?v=TdwUGOxCdUc), the accompanying [Lecture38.pdf](https://www.lithoguru.com/scientist/CHE323/Lecture38.pdf), [Semiconductor Lithography (Photolithography) - The Basic Process](https://www.lithoguru.com/scientist/lithobasics.html), and *Fundamental Principles of Optical Lithography: The Science of Microfabrication* (Wiley, 2007), section 1.3, pp. 12-26. Figures 1 and 5 reproduce slides 8 and 6 from the 2013 lecture; Figures 2 and 3 are the website's Figures 1-4 and 1-6; Figure 4 is the textbook's Figure 1.21, p. 23. Original figures and their content are retained, with PDF crops used for layout. The process-count annotation in Figure 5 belongs to the 2013 lecture.

