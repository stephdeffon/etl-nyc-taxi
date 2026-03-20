# Quality rules

These rules are applied in the cleaning step (`clean_df`) from `src/transform.py`.

- Keep only trips with `fare_amount > 0`.
- Keep only trips with `trip_duration > 0` (in minutes).
- Keep only trips where `tpep_pickup_datetime < tpep_dropoff_datetime`.
- Replace missing `passenger_count` with `0`, then keep only trips with `passenger_count > 0`.
