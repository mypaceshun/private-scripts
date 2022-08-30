# 様々なフォーマット手法の速度を計測した

いきなり結論 -> f-stringが一番早かった

# 実行手順

```
$ poetry install
$ poetry run test
```

# 実行結果

```
run script num=10000000
          format_run start: 2022-08-30 12:49:46.178620
          format_run   end: 2022-08-30 12:49:50.786314
          format_run total: 4.607694
         fstring_run start: 2022-08-30 12:49:50.790880
         fstring_run   end: 2022-08-30 12:49:53.689108
         fstring_run total: 2.898228
         percent_run start: 2022-08-30 12:49:53.693739
         percent_run   end: 2022-08-30 12:49:57.595918
         percent_run total: 3.902179
      pre_format_run start: 2022-08-30 12:49:57.597856
      pre_format_run   end: 2022-08-30 12:50:02.435619
      pre_format_run total: 4.837763
     pre_percent_run start: 2022-08-30 12:50:02.440995
     pre_percent_run   end: 2022-08-30 12:50:06.581255
     pre_percent_run total: 4.14026
         logging_run start: 2022-08-30 12:50:06.589823
         logging_run   end: 2022-08-30 12:50:11.937270
         logging_run total: 5.347447
            plus_run start: 2022-08-30 12:50:11.948973
            plus_run   end: 2022-08-30 12:50:17.028131
            plus_run total: 5.079158
```
