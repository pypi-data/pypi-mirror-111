# README

This lib implements a lot of methods to use in `Python` + `Selenium` + `Allure` projects.

## Common methods

### c_log

Prints log message to allure report

Params:

* `severity` one of the available logging levels (`error`, `warning`, `info`, `debug`)
* `message` printable message

Example:

```python
c_log('info', f'Message to print')
```

### c_screeshot

Takes screenshot and attaches it to allure report

Params:

* `browser` webdriver instance
* `name` screenshot name

Example:

```python
c_screeshot(context.browser, 'Screenshot')
```

### c_wait

Waits specified number of seconds for something incredible

Params:

* `delay` time to wait in seconds

Example:

```python
c_wait(5)
```

### c_store

Saves value to variable in store

Params:

* `store` store where to save
* `variable` variable when to save
* `value` value to be saved

Example:

```python
c_store(context, 123, 'var')
```

### c_assert_condition

Checks that condition is true

Params:

* `condition` condition to check
* `message` printable message

Example:

```python
c_assert_condition(condition, f'Condition is not true')
```

### c_assert_equals

Checks that expected value equals to real value

Params:

* `expected` value that we expect
* `real` actual value
* `message` printable message

Example:

```python
c_assert_equals(expected, real, f'Expected value not equal to real value')
```

### c_assert_contains

Checks that substring contains in string

Params:

* `needle` substring to contain
* `haystack` string that should contain
* `message` printable message

Example:

```python
c_assert_contains(needle, haystack, f'Haystack does not contain needle')
```

### c_assert_matches

Checks that string matches regular expression

Params:

* `string` string that should match
* `regex` regular expression to search
* `message` printable message

Example:

```python
c_assert_matches(string, regex, f'String does not match regex')
```

### c_assert_json_valid

Checks that the JSON is valid

Params:

* `jsonData` checked JSON
* `message` printable message

Example:

```python
c_assert_json_valid(jsonData, f'Provided JSON is not valid')
```

## Frontend methods

### f_open

Opens specified url

Params:

* `browser` webdriver instance
* `url` url to open

Example:

```python
f_open(context.browser, 'http://tested-resource.org/')
```

### f_click

Clicks on LMB over element

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_click(context.browser, xc['selector'])
```

### f_send_keys

Types text or hits control keys over the element

Params:

* `browser` webdriver instance
* `selector` selector to the element
* `value` input text or control key

Example:

```python
f_send_keys(context.browser, xc['selector'], 'Hello')
```

### f_assert_enabled

Checks that the element is enabled

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_enabled(context.browser, xc['selector'])
```

### f_assert_not_enabled

Checks that the element is not enabled

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_not_enabled(context.browser, xc['selector'])
```

### f_assert_displayed

Checks that the element is visible

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_displayed(context.browser, xc['selector'])
```

### f_assert_not_displayed

Checks that the element is not visible

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_not_displayed(context.browser, xc['selector'])
```

### f_assert_exists

Checks that the element is presented

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_exists(context.browser, xc['selector'])
```

### f_assert_not_exists

Checks that the element is not presented

Params:

* `browser` webdriver instance
* `selector` selector to the element

Example:

```python
f_assert_not_exists(context.browser, xc['selector'])
```

### f_assert_equals

Checks that the attribute of the element equals to the expected value

Params:

* `browser` webdriver instance
* `selector` selector to the element
* `attr` checked attribute
* `expected` expected value

Example:

```python
f_assert_equals(context.browser, xc['selector'], 'value', 'Hello')
```

### f_assert_not_equals

Checks that the attribute of the element not equals to the expected value

Params:

* `browser` webdriver instance
* `selector` selector to the element
* `attr` checked attribute
* `expected` expected value

Example:

```python
f_assert_not_equals(context.browser, xc['selector'], 'value', 'Hello')
```

### f_assert_contains

Checks that the attribute of the element contains the expected value

Params:

* `browser` webdriver instance
* `selector` selector to the element
* `attr` checked attribute
* `expected` expected value

Example:

```python
f_assert_contains(context.browser, xc['selector'], 'value', 'Hello')
```

### f_assert_not_contains

Checks that the attribute of the element is not contains the expected value

Params:

* `browser` webdriver instance
* `selector` selector to the element
* `attr` checked attribute
* `expected` expected value

Example:

```python
f_assert_not_contains(context.browser, xc['selector'], 'value', 'Hello')
```

## Backend methods

### b_request

Sends request to specified api with specified params

Params:

* `method` one of the available methods (`get`, `post`, `put`, `patch`, `delete`)
* `url` url to request
* `data` *optional* Dictionary or list of tuples
* `headers` *optional* Dictionary of HTTP Headers to send
* `files` *optional* Dictionary of `'name': file-like-objects`

Return:

* `Response <Response>` object

Example:

```python
b_request('GET', '/reports')
b_request('POST', '/reports', headers=headers, data=data)
```
