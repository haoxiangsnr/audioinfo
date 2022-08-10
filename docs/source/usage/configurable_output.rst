Configurable Output
===================

Using audioinfo can generate personalize data. Depending on the different
tasks, the custom output can be achieved using the ``output_members``.

Supported output members
------------------------

During the simulation, without affecting the simulation speed, audioinfo
will collect the supported output members as much as possible.

Based on the effectiveness, the number of output members can be stored
in the disks, which is optimized by the arrow system.

 ============================= ==================================================================================================================
  Method                       Description
 ============================= ==================================================================================================================
  ``mix_y``                      signals mixed by dry clean source signals.
  ``mix_y_rvb``                  signals mixed by reverberant clean signals.
  ``mix_y_rvb_direct_path``      like ``mix_y_rvb``, but only with direct-path part.
  ``mix_y_rvb_early``            like ``mix_y_rvb``, but only with early-path part.
  ``mix_y_rvb_late``             like ``mix_y_rvb``, but only with late-path part.
  ``n_mix_y``                    ``mix_y`` with noise added.
  ``n_mix_y_rvb``                ``mix_y_rvb`` with noise added.
  ``n_mix_y_rir_direct_path``    ``mix_y_rvb_direct_path`` with noise added.
  ``n_mix_y_rir_early``          ``mix_y_rvb_early`` with noise added.
  ``n_mix_y_rir_late``           ``mix_y_rvb_late`` with noise added.
  ``s_<id>_y``                   dry clean signals with the id ``<id>``. If the number of speakers is 1, you can use ``s_y``. The same applies below
  ``s_<id>_y_rvb``               reverberant clean signals with the id ``<id>``.
  ``s_<id>_y_rvb_direct_path``   like ``s_<id>_y_rvb``, but only use direct-path part.
  ``s_<id>_y_rvb_early``         like ``s_<id>_y_rvb``, but only use early reflection.
  ``s_<id>_y_rvb_late``          like ``s_<id>_y_rvb``, but only use late reflection.
  ``s_<id>_rvb_peak_idx``        peak index of room impulse response of the source with the id ``<id>``.
  ``s_<id>_y_vad``               voice activity detection result of the source with the id ``<id>``.
  ``s_<id>_vad``                 voice activity detection label (0 or 1) of the source with the id ``<id>``.
  ``s_<id>_transcript``          transcript of the source with the id ``<id>``.
  ``s_<id>_traj``                trajectory of the source with the id ``<id>``.
  ``s_<id>_doa``                 direction of arrival of the source with the id ```<id>``` (in degree).
  ``s_<id>_timestamps``          timestamps of the signal with the id ```<id>```.
  ``n_y``                        noise signals.
  ``n_gain``                     noise gain.
 ============================= ==================================================================================================================


In your config file, you can specify the ``output_members``. For
instance, if you want to do single-channel speech enhancement without
reverberation, you may specify the following members:

.. code:: py

   from audioinfo import ConfigurableWriter
   output_members=["n_mix_y", "s_y", "n_y"]

For multichannel two-speaker localization/tracking with additive noise
and reverberation, you may:

.. code:: py

   output_members=["n_mix_y_rvb", "s_1_traj", "s_2_traj", "s_1_doa", "s_2_doa", "n_y"]

For multichannel single-speaker speech recognition with noise and
reverberation, you may:

.. code:: py

   output_members=["n_mix_y_rvb", "s_y", "s_transcript"]

For multichannel dereverberation with noise and reverberation, you may:

.. code:: py

   output_members=["n_mix_y_rvb", "s_y_rvb_direct_path"]

Then, you can initialize the configurable writer:

.. code:: py

   writer = ConfigurableWriter(output_members=output_members)

.. automodule:: audioinfo.rir_simulator
   :members:
   :undoc-members: