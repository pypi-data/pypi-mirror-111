# utils

Implements simple extensions to the core python libraries.

To install a stable version:

```
pip install utils-nuuuwan
```

To install a pre-release (which might have more features, but also be
less stable):

```
pip install -i https://test.pypi.org/simple/ utils-nuuuwan
```

# Release History
See also [Older Releases](OLDER_RELEASES.md) and [Wish-list](WISHLIST.md)

## 1.0.19

* Fixed download bug in Browser
* Added *sysx*.retry

## 1.0.18

* Added default unixtime to timex.get_date_id
* Renamed Module *browser* to *browserx*
* Added auto download for other filetypes in *browserx*
* Added various utils to *browserx*

## 1.0.17

* Added timex.get_date_id

## 1.0.16

* Added module *open_browser* with open
* Added module *image*, with crop and resize
* Added more loggiing to *twitter*

## 1.0.15

* Fix various bugs in *cache*

## 1.0.14

* Added GeoDataFrame support in *cache*.

## 1.0.13

* Added MultiPolygon and other geometry support to *cache*

## 1.0.12

* Added pandas.DataFrame support to *cache*

## 1.0.11

* Added caching to www.read
