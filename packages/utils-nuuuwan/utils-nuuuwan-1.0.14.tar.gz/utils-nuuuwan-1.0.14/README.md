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

## 1.0.14

* Added GeoDataFrame support in cache.

## 1.0.13

* Added MultiPolygon and other geometry support to cache

## 1.0.12

* Added pandas.DataFrame support to cache

## 1.0.11

* Added caching to www.read

## 1.0.10

* Add parse int
* Add SECONDS_IN constants to *timex*
* Added module *twitter*

## 1.0.9

* Reverted Timezone Support
* Added timex.get_timezone

## 1.0.8

* Added timezone support

## 1.0.7

* Fixed bug with selenium import

## 1.0.6 (DO NOT USE - WILL BREAK utils.www)

* Added ds.sort_dict_items_by_key

## 1.0.5 (DO NOT USE - WILL BREAK utils.www)

* Added *use_selenium* option to *www.read*
* Added *www.get_all_urls*
* Added *sys.str_color*

## 1.0.4

* Added *www.exists*
* Added *timex.format_time*

## 1.0.3

* Added New Module *hashx* with md5 hashing
* Added New Module *filex* with read and write
* Added download_binary in Module *www*


## 1.0.2

* Fixed breaking bug in Module *cache* timeout logic.

## 1.0.1 (DO NOT USE - WILL BREAK utils.cache)

* Added get_unixtime and parse_time to Module *timex*.
* Fixed big in timeout logic in Module *cache*

## 1.0.0

- Initial Release. See source for details


## Wishlist
