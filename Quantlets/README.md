# EMQA Quantlets

One Quantlet per chart of the lectures, as in the MFM and SFM courses:

```
Quantlets/Lk/EMQA_Lk_<chart>/
    Metainfo.txt            name, description, keywords, data, output
    EMQA_Lk_<chart>.ipynb   self-contained notebook (executed): loads the course data, computes, draws the chart
    <chart>.png             the chart
Quantlets/Data/EMQA_data/   how the course data are downloaded (data/download_all.py) and how to load each series
```

* Each notebook runs on its own, locally or on Google Colab. It reads the data from `data/clean` of a local copy of
  the repository, or from the public repository on GitHub.
* The numbers printed by a notebook are those on the slide.
* Every slide with a chart links the Quantlet of that chart (bottom right), and each Quantlet is built by
  `lectures/Lk/make_quantlets_Lk.py` with the helper `lectures/common/emqa_quantlet.py`.
