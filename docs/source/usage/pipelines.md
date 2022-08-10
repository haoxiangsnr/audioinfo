# Organization of Pipelines

简单来说，我们可选的调用方式一般理来说有三种：
- console script：给定一个 main 入口，程序会将这些代码汇总到程序中，之后开始进行调用了。
- simulation recipe：如果你想要自定义的话，那你可以使用 simuation recipe 来实现哈。
- package reference：package reference 与 simulation recipe 相似。可以参考 simulation 来自己实现仿真过程。

三者之间的关系：

- main 函数其实就是简化版本的接口，我们先提供 main 函数，自动支持默认的数据集。
- 对于其他数据集，我们会构建示例的 simulation recipe，你可以直接调用。
- package reference 相对非常松散，你可以加载一些核心的接口，来自己实现接口以外的东西。

## Console script

```shell
audioinfo \
  --clean_data_path=<clean_data_path> \
  --noise_data_path=<noise_data_path> \
  --snr_range=2,3 \
  --num_spks=2 \
...
```

## Simulation recipe

```shell
cd </path/to/project>
python simulate.py --config_file recipes/train.toml
```

## Package reference

```shell
from audioinfo import mixer

# user-defined parameters
clean_fpath_list = "./data/clean_data/clean_data_list.txt"
noise_fpath_list = "./data/noise_data/noise_data_list.txt"

#
mixture = mixer.mix(clean, noise, rirs)
```

```python
# 传统的 clean dataset
preprocessing.py = > clean_dataset

# database => Dataloader => return Sources
# __iter__，__next__ 等等应该如何设计，如果遍历，那么就顺序，否则就是随机生成？或者给一个专门的接口吧
# How to select sources from the different speakers?
source_loader = Dataloader(dataset, parallel_preload, num_sources, shuffle, sample_rate, include_vad, max_norm
use_cache, cache_args = {max_cache, cache}, label = "")
noise_loader = Sourceloader(...)
rir_loader = ...
mic = Mic(array_arch)
room_loader = Roomloader(roomsize, min_allowable_distance_to_wall, angle_dist, use_elevation)
rir_simulate = RIRSimulator(backend="pyroom")
traj_generator = Trajectory_generator(min_allowable_distance_to_wall, use_elevation, use_azimuth, additional
databases, types = [""])

# 传统的 clean piplines
# 将 pipeline 中的复杂度降低，这样你可以走多个 pipelines
for (sources:list[Source], noise: Source, room: Room, mic) in sources_loader:
    noise: Source = next(noise_loader)  # 或者 noise_loader.sample(外部参数)，实际上就是给一个 random seed 而已，哈哈
    room: Room = room_generator.create()  # 包含房间，墙，以及相关的系数
    sources_traj = Trajectory_generator.generate(num_spk, sources: 时长)  # with random type
    rirs = rir_simulate.simulate_rirs(sources, mic, room, rir_interval)  # 将 room 与 traj 等信息全部给到仿真器

    # Source has y_rir, y_rir_early, ...
    mix_source = mix(sources, noise, overlap_rate, target_loudness_level, floating_range_target
    loudness_level, mix_mode)
    # steps，没有什么是可以替代思考的，思考就像跑步，不思考就会越来越慢

    # 0. normalize sources gains.
    # 1. source.gains = mixer.sample_source_gains(clean_num_sources)  # 因为要控制总体平均，所以需要使用类，而不是函数, (-5, -3, ...)
    # 2. noise.gains = mixer.sample_noise_grans(1)  # 也要控制总体
    # 4. apply gains
    #

    # for-loop mixture, sources, noise
    filter_options(output_options):
    ...
    name = "source_4_1_noise_2_2_"
```

- [x] 如果单条的噪声的长度很长呢？不用 pre_load 的时候就会特别的慢，使用 cache 来加速，随你怎么用
- [x] 考虑一下上面列出的重要参数
- [ ] 是否有必要提前做 fit length 呢？问题点是什么呢？不应该先做 fit length 啊，考虑一条语音较短时，有效语音总是很好的
- [x] additional databases 要如何用呢？还是单独变成一个类吧，就和噪声一样了
- [x] early_late_split. may add an arg `split_rir`
- [x] which type of output，使用 valid_options + custom_options，可能会没有的，要给出 warning 啊，参考
    - https://github.com/pypa/setuptools/blob/main/setuptools/dist.py#L191
    - https://github.com/readthedocs/sphinx-autoapi
- [x] angle_dist，和师兄聊一下这个吧，看看他是如何划分和采样的，要看的东西还很多
- [x] Transcript 要如何放置呢？