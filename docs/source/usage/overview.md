# Overview

audioinfo is an open-source multipurpose speech mixture simulator that
covers speaker localization/tracking, dereverberation, enhancement,
separation, and recognition tasks.

## TODO

-   [ ] add a logger to generate output files
-   [ ] add a report with the header that has an overview table and
    details
-   [ ] may add continue to simulate?
-   [ ] support additional real RIRs?
    https://github.com/jonashaag/RealRIRs

## Motivation

**More realistic**: The typical open-source datasets available today are
relatively simple. For example, the WSJ0-2Mix dataset[^1] contains
only two speakers, no noise, and a small amount of data. Models trained
on these datasets do not generalize to real-world scenarios, e.g.,
Conv-TasNet, which achieves optimal performance, when acoustic
conditions change slightly, does not work well[^2]. This simulator
can set parameters such as reverberation, noise, number of sources,
source location, source movement trajectory, speech overlap rate, etc.,
closer to the natural acoustic scene.

**More reproducible**: The vast majority of the papers use
non-open-source simulation datasets. Although the authors describe the
configuration of the dataset in the implementation section in as much
detail as possible, it is still difficult for the reader to simulate the
same dataset. Many papers' datasets and data simulation scripts are not
publicly available, making it impossible to reproduce and further
analyze the model performance by tuning the data generation. Moreover,
directly sharing their datasets on the Internet is lengthy and slow.
This simulator ensures reasonability and treats reproducibility as a
first-class thing. Using
the [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
of the GitHub, the authors of papers can publish their configuration
file to this repository. This repository will exhibit the configuration
file and associate it with your paper and system details. We will keep
the reproducibility of using your configuration file in the future.

**More general**: Unlike the commonly used datasets [LibriMix](https://github.com/JorisCos/LibriMix) only for
separation, [DNS](https://github.com/microsoft/DNS-Challenge) for only
denoising, [LibriCSS](https://github.com/chenzhuo1011/libri_css) only for separation and ASR), the simulated datasets
using this simulator can
cover many tasks such as localization, tracking, enhancement,
separation, dereverberation, and recognition. Only the required output
targets need to be defined through configuration files. In addition,
commonly used baseline models and algorithms are included in the example
recipes. Based on the example recipes, we will analyze the importance of
common parameters (SNR, reverberation time, and the number of sources)
on the performance of each subtask.

## Features

In this simulator, you can or will be able to:

**Use flexible parameters**: By customizing various parameters, the
simulator produces a mixture closer to a natural scene than the common
dataset. By customizing the output parameters, the simulator can
generate datasets suitable for various tasks, including
localization/tracking, denoising, dereverberation, separation and
recognition.

**Share your configuration**: Push your scripts to this repository by
the [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
, and we will use GitHub Actions to post your configuration on a showcase
page (in the future), including the corresponding paper, dataset size
and system details (python version, dependencies versions), etc. We will
also support automatic syncing of the simulated datasets to the [Zenodo](https://www.zenodo.org/)
and [Hugging Face](https://huggingface.co/). In this way, your dataset
is reproducible, and others can efficiently conduct comparisons and
experiments based on your dataset.

**Use multiple calling methods**: Use both offline and online calling
methods. In offline calling, for simple tasks, you can use the simulator
directly with console scripts, like:

```shell
audioinfo\
--clean_data_path=`<clean_data_path>`{=html}\
--noise_data_path=`<noise_data_path>`{=html}\
--snr_range=2,3\
--num_spks=2\
...
```

For complex simulation tasks, you can build the dataset via the
simulation recipe in the project recipe directory, like:

```shell
cd /path/to/project
audioinfo --config_file recipes/train.toml
```

Supposing that you do not want to store many data on the local disk but
have a sufficient memory size, you can use the simulator directly during
`PyTorch Dataloader <https://pytorch.org/docs/stable/data.html>` iterations through the package reference, like:

```python
from audioinfo import mixer

mixture = mixer.mix(clean, noise, rirs)
```

Later, we will provide practical documentation of the core interface and
examples via the Jupyter notebook.

**Not Included Features**

This simulator aims to obtain a realistic mixture (as much as possible)
using the given parameters and strictly keep the reproducibility. It
includes preprocessing speech and noise databases and more realistic
source mixing. We hope this simulator will help the algorithm and model
design within the far-field speech signal processing. These are what
this simulator does. This simulator will not include the complex and
advanced parameters of RIR simulation, such as directional microphones
and complex microphone architectures. Also, this simulator does not aim
for data augmentation, like time stretch, pitch shifting, etc.

## Main Components

This simulator contains three core components that are Dataloader, RIR
Simulators, and Mixer. The process is modularized so that many scenarios
can be created by slightly changing the pipeline. We will provide
example recipes and classes to show how the single modules are used. If
a scenario is not supported, new modules can be easily implemented to
adapt this simulator to your requirements.

![main](https://user-images.githubusercontent.com/28479613/176113289-e1c0ec72-0de3-4f43-841e-0118659fb61d.png)

### Dataloader

![dataloader](https://user-images.githubusercontent.com/28479613/176113708-99da6d36-7432-40b4-b87c-ccfa9b47ec6b.png)

The dataloader defines the loading, preprocessing, and iteration of the
dataset. Basically, the dataloader is responsible for reading the speech
and noise datasets from the database. The speech and noise datasets are
paired together to produce the required amount of speech and noise for
each iteration and perform normalization operations such as maximum
loudness normalization (Max Norm), etc. Any clean database consisting of
single-speaker utterances that provides access to speaker identities can
be used to simulate data. Any additional information like transcriptions
is kept and can still be used. The dataloader supports WSJ-0 and [AISHELL-3](https://www.aishelltech.com/aishell_3) by
default. The environmental noises (e.g., from [WHAM!](https://wham.whisper.ai/)) are supported.

Parameters supported by the plan:

- `num_spks` : the number of speakers needed for multi-speaker cases
- `parallel_preload` : whether to parallel load and cache the database in memory in advance. For
  frequently used data, like noise
- `shuffle` : whether to shuffle the data
- `sample_rate` : sampling rate
- `save_vad` : when the SNR of the speech database is low, after convolution of RIR, the noise is
  directional. This parameter is for speaker localization and tracking

### RIR Simulator

![rir_sim](https://user-images.githubusercontent.com/28479613/176113667-13787ed1-8876-4693-a4e8-99008deefacd.png)

RIR Simulator simulates dynamic or static RIRs based on given room
parameters, microphone (like architecture and position), and source
position parameters. It contains subcomponents such as a room generator,
trajectory generator, and microphone architecture generator. - The room
generator samples room-related parameters based on the given room range,
wall reflection coefficients, etc., and provides functions such as wall
collision detection. - The trajectory simulator generates static
positions or dynamic trajectories. You can specify the angle
distribution between the target and the interfering sources if the case
is multiple static sources. - Use the microphone architecture generator
to generate some standard microphone arrays.

Parameters supported by the plan:

- `array_arch` : supports predefined standard circular arrays (specifying radius and number), line arrays
  (specifying fixed or non-spaced intervals)
- `t60_range`
- `room_size` :range of room sizes. Currently, only convex hexahedral rooms to be supported (gpuRIR only supports convex
  hexahedral rooms)
  -`room_absorption_coefficient` : individual wall reflection coefficients
- `min_allowable_distance_to_wall` : minimum source-to-microphone distance from the wall
- `angle_dist` : angular distribution between the target and interfering sound sources. The angle distribution will
  converge to the desired ratio after the dataset simulation is completed
- `trajectory_types` : the types of trajectories to be simulated
- `use_elevation` : generate elevation angle for localization and tracking
- `use_azimuth` : generate azimuth angle for localization and tracking
- `use_distance` : generate the distance from the sound source to the microphone, used for localization and tracking
- `rir_interval` : how often the RIR is simulated
- The additional databases that provide room impulse responses
- Early-Late reflection split, which is commonly used for dereverberation - ...

### Mixer

![mixer](https://user-images.githubusercontent.com/28479613/176113744-aede1244-3c9c-4f60-8397-0116c5dc7cb1.png)

The mixer mixes the speech sources and background noise. Precisely, it
first does a basic check of the relevant configuration. Then it
determines the early response of the signal (when it contains
reverberation) by peak checking, unifies the loudness, and generates a
mixture.

Parameters supported by the plan:

- `overlap_ratios` : in natural conversations, speech signals are continuous and contain both overlapped and
  overlap-free regions, which can be specified
  -`target_loudness_level` : a given level for loudness normalization
- `floating_range_target loudness level` : a given limit for loudness normalization
- `mix_mode` : support "min" (the mixture ends when the shortest source ends), "max" (the mixture ends with the longest
  source, and the shorter source will start at a random position). It is used when the `overlap_ratios` is set to 100%
- `snr_range`
- `sir_range`

### Configurable Writer

For different tasks, by using a configurable writer, you can output the
desired audio signals and other information, like

- Clean Mixture
- Noisy mixture
- Direct-path impulse responses (DPIRs) and the filtered
- Early-path impulse responses (EPIRs) and the filtered
- Room impulse responses (RIRs) and the filtered
- Transcriptions
- Brief report, including the number of files, the total hours, etc.
- ...

## Roadmap Planning

The basic idea is first to build a simulator system that is **easily
scalable**, **easy to participate in**, and **well-structured** **before
August**. In the functional aspect, this simulator fully satisfies the
demand for multi-channel multi-speaker speech recognition in dynamic
environments.

After July, the main tasks are to give mainstream baselines on an
example recipe, extend the calling method, support sharing, and publish
other people's recipes.

### Planned before Aug.

- Jun. 21 to Jun. 28

    -   [x] Initial build process
        (`Setuptools <https://github.com/pypa/setuptools>`**), test
        process (`pytest <https://docs.pytest.org/en/7.1.x/>`**),
        auxiliary tools (formatter), libraries
        (`GitHub    Actions <https://github.com/features/actions>`**)
        and documentation generation
        (`readthedocs.org <https://readthedocs.org/>`**)

- Jun. 29 to Jul. 5

    -   [ ] Refactor previous dataloader to configurable
    -   [ ] Support the parameters of dataloader listed above
    -   [ ] Support the `WHAM! <http://wham.whisper.ai/>`\_\_ noise
        dataset
    -   [ ] Support dataset composition
    -   [ ] Implement mixer, support the parameters listed above

- Jul. 6 to Jul. 12

    -   [ ] Implement RIR Simulator based on the old code
    -   [ ] Support the parameters of RIR Simulator listed above

- Jul. 13 to Jul. 19

    -   [ ] Design version system for reproducible simulation through
        (maybe) locking versions of simulator and dependencies,
        collecting metadata (spitted length, start position of slicing,
        etc.), during the simulating.
    -   [ ] Design the structure of configuration and implement parser
        and validator of configuration file
    -   [ ] Implement configurable writer

- Jul. 20 to Jul. 26

    - Add basic documents, like tutorials.
    - Implement baseline methods

### After

-   [ ] Implement mainstream baselines on each task based on an example
    recipe. Moreover, give a brief analysis.

-   [ ] (Cannot make sure) Support sharing and publishing the
    configuration file and dataset meta information on a showcase page
    by the Pull Request.

-   [ ] Support for calling basic functions through the console scripts,
    like `audioinfo --clean_data_path=... --noise_data_path=... --snr_range=2,3 num_spks=2 ...`

-   [ ] Support for using any additional database that provides room
    impulse responses

-   [ ] (Cannot make sure) Support for generating the classical speech
    mixture scenarios

    - WSJ0-2mix/WSJ0-3mix
    - LibriCSS

-   [ ] Add more documents

[^1]: Hershey, John R., et al. "Deep clustering: Discriminative
embeddings for segmentation and separation." 2016 IEEE international
conference on acoustics, speech and signal processing (ICASSP). IEEE, 2016.

[^1]: Kadıoğlu, Berkan et al. "An Empirical Study of Conv-Tasnet."
ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech
and Signal Processing (ICASSP) (2020): 7264-7268.
