Overlap Ratio
=============

Different overlap ratios [1]_ can be applied in the audioinfo. To create the overlapped mixture, we randomly shift the onset of each.
Sometimes to avoid the long tail produced by long reverberation causes the overlapping of the consecutive speech utterance from the same speakers, you may assign a minimum silence length in the settings. To be clear, assigning the minimum silence length will add a short silence interval with the given length, in samples, to the consecutive utterances of the same speakers.

In the calculation of the overlap ratio, we use

.. math::
    \text{ovp} = \frac{L_\text{overlap}}{L_\text{total}}

where the :math:`L_\text{overlap}` and :math:`L_\text{total}`  are the total length of the overlapped speech and entire mixture length, respectively.


.. [1]
    Çetin, Özgür and Elizabeth Shriberg. “Analysis of overlaps in meetings by dialog factors, hot spots, speakers, and collection site: insights for automatic speech recognition.” INTERSPEECH (2006).