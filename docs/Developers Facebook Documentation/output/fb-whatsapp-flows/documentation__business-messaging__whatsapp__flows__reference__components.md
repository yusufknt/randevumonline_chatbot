# Components | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components_

---

# Components

Updated: Apr 14, 2026

Components are like building blocks. They allow you to build complex UIs and display business data using attribute models. **The maximum number of components per screen is 50.** Please refer to [best practices for components](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/guides/bestpractices#number-of-components).

The following components are supported:

- [Basic Text (Heading, Subheading, Caption, Body)](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#text)
- [RichText](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#richtext)
- [TextEntry](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#textentry)
- [CheckboxGroup](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#checkbox)
- [RadioButtonsGroup](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#radio)
- [Footer](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#foot)
- [OptIn](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#opt)
- [Dropdown](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#drop)
- [EmbeddedLink](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#embed)
- [DatePicker](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#dp)

- [CalendarPicker](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#calendarpicker)

- [Image](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#img)
- [If](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#if)
- [Switch](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#switch)
- [Media upload](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#media_upload)

- [NavigationList](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#navlist)

- [Chips Selector](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#chips_selector)

- [Image Carousel](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#image_carousel)

## Text Components

### Heading

This is the top level title of a page.

| Parameter | Description |
| --- | --- |
| `type` *string* | **Required.** “TextHeading” |
| `text` *string* | **Required.** Dynamic “${data.text}” |
| `visible` *boolean* | Dynamic “${data.is_visible}”<br>Default: True |

### Subheading

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “TextSubheading” |
| `text _string_`(required) | Dynamic “${data.text}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |

### Body

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | TextBody |
| `text _string_`(required) | Dynamic “${data.text}” |
| `font-weight _enum_` | {‘bold’,’italic’,’bold_italic’,’normal’} <br>Dynamic “${data.font_weight}” |
| `strikethrough _boolean_` | Dynamic “${data.strikethrough}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `markdown _boolean_` | Default: False<br>Requires Flow JSON V5.1+ |

### Caption

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “TextCaption” |
| `text _string_`(required) | Dynamic “${data.text}” |
| `font-weight _enum_` | {‘bold’,’italic’,’bold_italic’,’normal’} <br>Dynamic “${data.font_weight}” |
| `strikethrough _boolean_` | Dynamic “${data.strikethrough}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `markdown _boolean_` | Default: False<br>Requires Flow JSON V5.1+ |

### Limits and Restrictions

| Component | Type | Limit / Restriction |
| --- | --- | --- |
| HeadingSubheadingBodyCaption | Character Limit | 80<br>80<br>4096<br>409 |
| Heading<br>Subheading<br>Body<br>Caption | Text | Empty or Blank value is not accepted |

### Additional capabilities for Text components

Supported starting with Flow JSON version 5.1

In Flow JSON V5.1 `TextBody` and `TextCaption` also supports a limited markdown syntax. In order to enable this capability, set the property `markdown=true`; this will instruct WhatsApp Flows to enable markdown syntax within these components.

```json
{
   "type": "TextBody",
   "markdown": true,
   "text": [
     "This text is ~~***really important***~~",
   ]
}
```

```json
{
   "type": "TextCaption",
   "markdown": true,
   "text": [
     "This text is ~~***really important***~~",
   ]
}
```

For comparison purposes, we show how the text components look like next to one another:

## Rich Text

Supported starting with Flow JSON version 5.1

Flow JSON 5.1 introduces a new component - `RichText`. The goal of the component is to provide a rich formatting capabilities and introduce the way to render large texts (**Terms of Condition**, **Policy Documents**, **User Agreement** and etc) without facing limitations of basic text components (**TextHeading**, **TextSubheading**, **TextBody** and etc)

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “RichText” |
| `_string \| string array_`(required)string \| string array | Dynamic “${data.text}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |

`RichText` component utilizes a select subset of the `Markdown` specification. It adheres strictly to standard `Markdown` syntax without introducing any custom modifications. Content created for the `RichText` component is fully compatible with standard `Markdown` documents.

**Note:**

Until V6.2, the RichText component can only be used as a standalone component on the screen and cannot be combined with other components on the same screen.

Starting with V6.3, the RichText component can be used in conjunction with the Footer component on same screen, allowing the Flow to navigate from or end at the screen with RichText.

If your use case requires to incorporate text with other components, consider using the basic Text component, which supports markdown features such as bold, italic, strikethrough, links and lists.

### Supported Syntax

Headings

The current syntax supports only `Heading (h1)` and `Subheading (h2)`. Other heading levels will be parsed but rendered as normal text - `TextBody`.

| Flow JSON | Flow Component |
| --- | --- |
| `{<br> "type": "RichText",<br> "text": [<br> "# Heading level 1",<br> ]<br>}` | `TextHeading` |
| `{<br> "type": "RichText",<br> "text": [<br> "## Heading level 2",<br> ]<br>}` | `TextSubheading` |
| `{<br> "type": "RichText",<br> "text": [<br> "### Heading level 3",<br> "#### Heading level 4",<br> "##### Heading level 5",<br> "###### Heading level 6",<br> ]<br> }` | `TextBody` |

Paragraphs

To create paragraphs, split your text into different array items:

```json
{
       "type": "RichText",
       "text": [
         "Paragraph 1",
        "Paragraph 2",
       ]
    }
```

or add a blank line in your markdown document that you bind using dynamic binding syntax `${data.your_dynamic_field}`

```json
# Heading 1
Paragraph 1

Paragraph 2
```

```json
{
       "type": "RichText",
       "text": "${data.text}"
    }
```

Text Formatting

| Flow JSON | Flow Component |
| --- | --- |
| `{<br> "type": "RichText",<br> "text": [<br> "Let’s make a **bold** statement",<br> ]<br>}` | `TextBody (bold)` |
| `{<br> "type": "RichText",<br> "text": [<br> "Let's make this text *italic*",<br> ]<br>}` | `TextBody (italic)` |
| `{<br> "type": "RichText",<br> "text": [<br> "Let's make this text ~~Strikethrough~~",<br> ]<br>}` | `TextBody (strikethrough)` |
| `{<br> "type": "RichText",<br> "text": [<br> "This text is ~~***really important***~~",<br> ]<br>}` | `TextBody (bold-italic-strikethrough)` |

Lists

You can organize items into ordered and unordered lists. At the moment, only single level lists are supported.

| Flow JSON | Flow Component |
| --- | --- |
| `{<br> "type": "RichText",<br> "text": [<br> "1. Item 1",<br> "2. Item 2",<br> "3. Item 3"<br> ]<br>}` | `OrderedList` (not available as standalone component) |
| `{<br> "type": "RichText",<br> "text": [<br> "- Item 1",<br> "- Item 2",<br> "- Item 3"<br> ]<br>}`<br>`{<br> "type": "RichText",<br> "text": [<br> "+ Item 1",<br> "+ Item 2",<br> "+ Item 3"<br> ]<br>}` | `UnorderedList` (not available as standalone component) |

Images

You can also include images in the content. Please note, external URIs are not supported and you can only include base64 inline images

```json
{
   "type": "RichText",
   "text": ["![Image alt text](data:image/png;base64,<base64 content>)"]
}
```

**Recommended image formats:**

1. png
2. jpg / jpeg
3. webp (please note, webp is only supported starting from IOS 14.6+, that corresponds to ~98% of IOS devices)

Links

To create a link, enclose the link text in brackets and then follow it immediately with the URL in parentheses

```json
{
   "type": "RichText",
   "text": [
     "[Whatsapp Flows are awesome](https://business.whatsapp.com/products/whatsapp-flows)",
   ]
}
```

Tables

| Column 1 | Column 2 |
| --- | --- |
| To add a table, use three or more hyphens (---) to create each column’s header, and use pipes ( | ) to separate each column. For compatibility, you should also add a pipe on either end of the row. |

Cell content can be combined with the following syntax:

1. Italic, bold, strikethrough
2. Images
3. Links

```json
{
   "type": "RichText",
   "text": [
     "\| Column Header 1     \| Column Header 2                                             \|",
     "\| -------------       \|  -------------                                              \|",
     "\| **Bold** text 1     \| [Link](<URI>)                                               |",
     "| **Bold** text 1     | ![Image alt text](data:image/png;base64,<base64 content>)   |",
   ]
}
```

**Width of the columns:**

Width of the column is based on the Header content size. Markdown specification doesn’t provide a specific syntax for controlling a column width. If you want to make a certain column wider, simply add additional content to the header:

```json
{
   "type": "RichText",
   "text": [
     "| Column Header 1 - Extended width  | Column Header 2       |",
     "| -------------                     |  -------------        |",
     "| **Bold** text 1                   | Cell text 2           |",
   ]
}
```

Working with large texts

If your text content for markdown has a limited size, you can incorporate it as a static text as shown in all examples above, however if your text is large and you expect to update it often on your server, we recommend sending it as a part of dynamic data, this will improve overall readability of the JSON and allow to load always up to date text from your server.

**Please note:** We use array text property for static cases since it’s easier to read. However the components support both types: `Array of strings` and `string`. Your markdown can be sent as a normal string, you don’t need to convert it to an array of strings.

Syntax cheatsheet

Supported starting with Flow JSON version 5.1

Here is the quick overview of the syntax that’s supported by RichText, TextBody and TextCaption components

| Syntax | RichText | TextBody | TextCaption |
| --- | --- | --- | --- |
| `# Text Heading` | ✅ | ❌ | ❌ |
| `## Text Subheading` | ✅ | ❌ | ❌ |
| `**bold**` | ✅ | ✅ | ✅ |
| `*italic*` | ✅ | ✅ | ✅ |
| `~~strikethrough~~` | ✅ | ✅ | ✅ |
| `Normal Paragraph` | ✅ | ✅ | ✅ |
| `+ Item 1<br>+ Item 2` | ✅ | ✅ | ✅ |
| `1. Item 1<br>2. Item 2` | ✅ | ✅ | ✅ |
| `[Link text](https://your-url.here)` | ✅ | ✅ | ✅ |
| `![Image Alt](data:image/png;base64, base64-data)` | ✅ | ❌ | ❌ |
| `\| Header 1 \| Header 2 \| Header 3 \|<br>\| -------- \| -------- \| -------- \|<br>\| Row 1 \| Data 1 \| More Data \|<br>\| Row 2 \| Data 2 \| More Data \|<br>\| Row 3 \| Data 3 \| More Data \|` | ✅ | ❌ | ❌ |

Usage example

## Text Entry Components

### TextInput

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “TextInput” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `input-type _enum_` | {‘text’,’number’,’email’, ‘password’, ‘passcode’, ‘phone’} |
| `pattern _string_` | When specified, it is a regular expression which the input’s value must match for the value to pass.<br>Supported starting with Flow JSON version 6.2Supported with input-type= {'text', 'number', 'password', 'passcode'}Expects a raw regex string (e.g., hello, not /hello/).When using the pattern field, helper-text is mandatory.For input-type= {'number', 'passcode' }, a base regular expression is applied before the pattern validator, ensuring both validations are performed. |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `min-chars _string_` | Dynamic “${data.min_chars}” |
| `max-chars _string_` | Dynamic “${data.max_chars}”. Default value is 80 characters. |
| `helper-text _string_` | Dynamic “${data.helper_text}” |
| `name _string_`(required) |  |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `init-value _string_` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |

### TextArea

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “TextArea” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `max-length _string_` | Dynamic “${data.max_length}” Default value is 600 characters. |
| `name _string_`(required) |  |
| `helper-text _string_` | Dynamic “${data.helper_text}” |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `init-value _string_` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |

### Limits and Restrictions

| Component | Type | Limit / Restriction |
| --- | --- | --- |
| TextInput | Helper Text<br>Error Text<br>Label | 80 characters<br>30 characters<br>20 characters |
| TextArea | Helper Text<br>Label | 80 characters<br>20 characters |

Together, the text entry components look like as shown:

## CheckboxGroup

CheckboxGroup component allows users to pick multiple selections from a list of options.

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “CheckboxGroup” |
| `data-source _array_`(required) | Dynamic “${data.data_source}”<br>Flow JSON versions before 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean>Flow JSON versions after 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string >Flow JSON versions after 6.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string, on-select-action: {name: 'update_data', payload: {...}}, on-unselect-action: {name: 'update_data', payload: {...}} > |
| `name _string_`(required) |  |
| `min-selected-items _int_` | Dynamic “${data.min_selected_items}” |
| `max-selected-items _int_` | Dynamic “${data.max_selected_items}” |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `label _string_` | Dynamic “${data.label}”<br>Flow JSON versions before 4.0: optionalFlow JSON versions after 4.0: required |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `on-select-action _action_` | `data_exchange` and `update_data` are supported.update_dataSupported starting with Flow JSON version 6.0 |
| `description _string_` | Dynamic “${data.description}”<br>Supported starting with Flow JSON version 4.0 |
| `init-value _array<string>` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Supported starting with Flow JSON version 4.0 |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component<br>Supported starting with Flow JSON version 4.0 |
| `media-size _enum_` | {‘regular’, ‘large’}<br>Dynamic “${data.media-size}”<br>Supported starting with Flow JSON version 5.0 |

Images in WEBP format are not supported on iOS versions prior to iOS 14.

### Example

For the `data-source` field, you can declare it dynamically or statically.

### Static Example

This static example hardcodes the respective `id`’s and `title`’s for the `data-source` field.

Dynamic Example

In this dynamic example, you can see that `data-source` references the `days_per_week_options` of type `array` defined before it using `days_per_week_options`. When defining such a structure, you need to specify `items` in the `array`, which will be of type `object`. Then inside the `items` object, you have a `properties` dictionary with `id` and `title` just like in the static declaration. Both `id` and `title` will always be of type `String`. Within the `days_per_week_options` array, you must define concrete examples in the `__example__` field.

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label Content<br>Title<br>Description<br>Metadata<br>Min # of options<br>Max # of options<br>Image | 30 Characters<br>30 Characters<br>300 Characters<br>20 Characters<br>1<br>20<br>Flow JSON versions before 6.0:<br>300KB<br>Flow JSON versions after 6.0:<br>100KB |

## RadioButtonsGroup

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “RadioButtonsGroup” |
| `data-source _array_`(required) | Dynamic “${data.data_source}”<br>Flow JSON versions before 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean>Flow JSON versions after 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string >Flow JSON versions after 6.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string, on-select-action: {name: 'update_data', payload: {...}}, on-unselect-action: {name: 'update_data', payload: {...}} > |
| `name _string_`(required) |  |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `label _string_` | Dynamic “${data.label}”<br>Flow JSON versions before 4.0: optionalFlow JSON versions after 4.0: required |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `on-select-action _action_` | `data_exchange` and `update_data` are supported.update_dataSupported starting with Flow JSON version 6.0 |
| `description _string_` | Dynamic “${data.description}”<br>Supported starting with Flow JSON version 4.0 |
| `init-value _array<string>` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Supported starting with Flow JSON version 4.0 |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component<br>Supported starting with Flow JSON version 4.0 |
| `media-size _enum_` | {‘regular’, ‘large’}<br>Dynamic “${data.media-size}”<br>Supported starting with Flow JSON version 5.0 |

Images in WEBP format are not supported on iOS versions prior to iOS 14.

### Example

For the `data-source` field, you can declare it dynamically or statically.

### Static Example

This static example hardcodes the respective `id`’s and `title`’s for the `data-source` field.

### Dynamic Example

In this dynamic example, you can see that `data-source` references the `experience_level_options` of type `array` defined before it using `data.experience_level_options`. When defining such a structure, you need to specify `items` in the `array`, which will be of type `object`. Then inside the `items` object, you have a `properties` dictionary with `id` and `title` just like in the static declaration. Both `id` and `title` will always be of type `String`. Within in the `experience_level_options` array you must define concrete examples in the `__example__` field.

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label Content<br>Title<br>Description<br>Metadata<br>Min # of options<br>Max # of options<br>Image | 30 Characters<br>30 Characters<br>300 Characters<br>20 Characters<br>1<br>20<br>Flow JSON versions before 6.0:<br>300KB<br>Flow JSON versions after 6.0:<br>100KB |

## Footer

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “Footer” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `left-caption _string_` | Dynamic “${data.left_caption}”<br>Can set left-caption **and** right-caption **or** only center-caption, but not all 3 at once |
| `center-caption _string_` | Dynamic “${data.center_caption}”<br>Can set center-caption **or** left-caption **and** right-caption, but not all 3 at once |
| `right-caption _string_` | Dynamic “${data.right_caption}”<br>Can set right-caption **and** left-caption **or** only center-caption, but not all 3 at once |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `on-click-action _action_`(required) | Action |

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label Max Character Limit<br>Captions Max Character Limit | 35<br>15 |

## OptIn

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “OptIn” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `name _string_`(required) |  |
| `on-click-action _action_` | Action that is executed on clicking “Read more”.<br>“Read more” is only visible when an on-click-action is specified.<br>Allowed values are `data_exchange` and `navigate`. From Flow JSON version 6.0 and later, allowed values are `data_exchange`, `navigate` and `open_url`. |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `init-value _boolean_` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |

### Example

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Content Max Character Limit<br>Max number of Opt-Ins Per Screen | 120<br>5 |

## Dropdown

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “Dropdown” |
| `label _string_`(required) |  |
| `data-source _array_`(required) | Dynamic “${data.data_source}”<br>Flow JSON versions before 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean>Flow JSON versions after 5.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string >Flow JSON versions after 6.0:Array< id: String, title: String, description: String, metadata: String, enabled: Boolean, image: Base64 of an image, alt-text: string, color: 6-digit hex color string, on-select-action: {name: 'update_data', payload: {...}}, on-unselect-action: {name: 'update_data', payload: {...}} > |
| `required _boolean_` |  |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `on-select-action _action_` | `data_exchange` and `update_data` are supported.update_dataSupported starting with Flow JSON version 6.0 |
| `init-value _string_` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component |

Images in WEBP format are not supported on iOS versions prior to iOS 14.

### Example

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label<br>Title<br>Min dropdown options<br>Max dropdown options<br>Description<br>Metadata<br>Image | 20 characters<br>30 characters<br>1<br>200 if no images are present in the `data-source`, 100 otherwise<br>300 characters<br>20 characters<br>Flow JSON versions before 6.0:<br>300KB<br>Flow JSON versions after 6.0:<br>100KB |

For the `data-source` field, you can declare it dynamically or statically.

Static Example

This static example hardcodes the respective `id`’s and `title`’s for the `data-source` field.

### Dynamic Example

In this dynamic example, you can see that `data-source` references the `experience_level_options` of type `array` defined before it using `experience_level_options`. When defining such a structure, you need to specify `items` in the `array`, which will be of type `object`. Then inside the `items` object, you have a `properties` dictionary with `id` and `title` just like in the static declaration. Both `id` and `title` will always be of type `String`. Within the `experience_level_options` array you must define concrete examples in the `__example__` field.

## Embedded Link

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “EmbeddedLink” |
| `text _string_`(required) | Dynamic “${data.text}” |
| `on-click-action _action_`(required) | Action<br>Allowed values are `data_exchange` and `navigate`. From Flow JSON version 6.0 and later, allowed values are `data_exchange`, `navigate` and `open_url`. |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Character limit | 25 |
| Case | No restriction on formatting |
| Max Number of Embedded Links Per Screen | 2 |
| Text | Empty or Blank value is not accepted |

## DatePicker

The DatePicker component allows users to input dates through an intuitive date selection interface.

Before Flow JSON version 5.0, the DatePicker doesn’t support scenarios where the business and the end user are in different
time zones. We recommend only using the component if you plan to send your Flows to users in a specific
timezone. For details, please refer to section
[Guidelines for Usage](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#datepicker-guidelines)Starting from Flow JSON version 5.0, the DatePicker has been updated to use a formatted date string in the format “YYYY-MM-DD”, such as “2024-10-21”,
for setting and retrieving date values. This update makes the date values of the date picker unrelated to time zones, allowing businesses to send messages and collect dates from users in any time zone.

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “DatePicker” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `min-date`String (timestamp in milliseconds) | Dynamic “${data.min_date}”. Please refer to section<br>[Guidelines for Usage](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#datepicker-guidelines) |
| `max-date`String (timestamp in milliseconds) | Dynamic “${data.max_date}”. Please refer to section<br>[Guidelines for Usage](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#datepicker-guidelines) |
| `name _string_`(required) |  |
| `unavailable-dates`Array < timestamp in milliseconds: String > | Dynamic “${data.unavailable_dates}”. Please refer to section<br>[Guidelines for Usage](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#datepicker-guidelines) |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `helper-text _string_` | Dynamic “${data.helper_text}” |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” <br>Default: True |
| `on-select-action _action_` | Only `data_exchange` is supported. |
| `init-value _string_` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component<br>Optional FormSupported starting with Flow JSON version 4.0 |

Payload that is sent to a data channel business endpoint is a string which shows the timestamp in milliseconds.

### Guidelines for Usage

### Before flow JSON version 5.0

Due to current system limitations, the DatePicker functions correctly and as intended(that is, correct selection range is shown to the User, and accurate user-selection value is returned to the Business) as long as

- The guidelines in this section are followed
- Both the business sending the Flow and its end-users are in the same time zone.

Correct behavior is not guaranteed if businesses and end-users are in different time zones. For example, if a business operating in Sao Paulo (UTC-3) sends a Flow to a user in Manaus (UTC-4), the DatePicker may not work as expected. We don’t recommend using it if your users are in different time zones than you.

Handling of Dates for Businesses and Users in the Same Time Zone

DatePicker allows setting of date range for user selection through `min-dates` and `max-dates` fields, and also prevents selection of specific dates using the `unavailable-dates` field. If you have not supplied the date range , then by default, the component allows the user to select dates from `1 January 1900` to `31 December 2100`.

**Setting Date Parameters in the Component**

When you specify the date range or set unavailable dates, you should convert your local dates with midnight (00:00:00) as a base time to UTC timestamps.

For example, if you are a business based in India who wants to collect a date in the range `21 March 2024` to `25 March 2024`, then you should set `min-dates` and `max-dates` as `1710958020000` and `1711303620000`, respectively.

`21 March 2024, 00:00:00.000 IST` converts to `20 March 2024, 18:30:00.000 UTC` which is represented by timestamp `1710958020000`.

`25 March 2024, 00:00:00.000 IST` converts to `24 March 2024, 18:30:00.000 UTC` which is represented by timestamp `1711303620000`.

**Component Integration**

DatePicker will read the timestamps in `min-dates`, `max-dates` and `unavailable-dates` fields and convert it to the end user’s local date for displaying on the UI. In the example we discussed above, a user in India will see dates from `21 March 2024` to `25 March 2024` in the DatePicker component.

**Processing User Selection**

Businesses will receive a UTC timestamp, which should be converted back to the business’s local time zone. Importantly, businesses should focus solely on the date portion of the resulting timestamp , disregarding the time portion. This ensures that the date remains consistent with the user’s selection. Unfortunately, this conversion will only work correctly when the business and user are in the same time zone.

For example, if you receive a timestamp `1711013400000` then convert it to your local timezone and extract the date. If you are in IST, the timestamp will convert to `21 March 2024 15:00 IST`, and you should treat `21st March 2024` as the user selected date.

Recommendation for navigating Time Zone differences

If you need to send flow messages to users in time zones different from yours despite reviewing the above guidelines, follow these steps to overcome the limitation:

- If you are a business based in Brazil and want to serve flows to your users across the country, then your time zone range will be `UTC-2 (Fernando de Noronha)` to `UTC-5 (Rio Branco)` .
- Add a `Dropdown` component within your Flow that allows users to select their current time zone.
- Identify the westernmost time zone from your time zone range. In our example, it is `UTC-5` .
- Provide the dates you want to collect in the westernmost time zone, using midnight as the reference time. For example, if you want to collect dates from `March 20th, 2024` to `March 25th, 2024` , then provide the timestamp in milliseconds for `March 20th, 2024 at 5 AM UTC` and `March 25th, 2024 at 5 AM UTC` .
- Convert the timestamps received from the user to their respective time zone and use the corresponding date. For example, if a user is in Sao Paulo(UTC-3) and you receive a timestamp of `1710910800000` , then convert it to `UTC-3` to get `March 20th, 2024` .

### Start from flow JSON version 5.0

DatePicker component has been updated to use a formatted date string in the format “YYYY-MM-DD”, such as “2024-10-21”, for setting and retrieving date values. This update makes the date values of the date picker unrelated to time zones, allowing businesses to send messages and collect dates from users in any time zone in a consistent manner.

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label Max Length | 40 characters |
| Helper Text Max Length | 80 characters |
| Error Message Max Length | 80 characters |

## CalendarPicker

Supported starting with Flow JSON version 6.1

The CalendarPicker component allows users to select a single date or a range of dates from a full calendar interface.

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “CalendarPicker” |
| `name _string_`(required) |  |
| `title _string_` | Dynamic “${data.title}” <br>Only available when ‘mode’ is set to ‘range’ |
| `description _string_` | Dynamic “${data.description}” <br>Only available when ‘mode’ is set to ‘range’ |
| `label _string_`(required) | Dynamic “${data.label}” <br>When ‘mode’ is set to ‘range’ the value should be in ‘{“start-date”: String, “end-date”: String}’ format |
| `helper-text _string_` | Dynamic “${data.helper_text}” <br>When ‘mode’ is set to ‘range’ the value should be in ‘{“start-date”: String, “end-date”: String}’ format |
| `required _boolean_` | Dynamic “${data.is_required}” <br>Default: False <br>When ‘mode’ is set to ‘range’ the value should be in ‘{“start-date”: Boolean, “end-date”: Boolean}’ format |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” <br>Default: True |
| `mode _enum_` | {“single”, “range”} <br>Dynamic “${data.mode}” <br>Default: “single” <br>Allows to select one date in ‘single’ mode or start and end dates in ‘range’ mode |
| `min-date _string_` | Dynamic “${data.min_date}” <br>Formatted date string in the format “YYYY-MM-DD” <br>Disallows selecting dates before specified min-date |
| `max-date _string_` | Dynamic “${data.max_date}” <br>Formatted date string in the format “YYYY-MM-DD” <br>Disallows selecting dates after specified max-date |
| `unavailable-dates _array<string>` | Dynamic “${data.unavailable_dates}” <br>Formatted date strings in the format “YYYY-MM-DD” <br>Disallows selecting specific dates, should be in the range between min-date and max-date if specified |
| `include-days`Array<enum> | {“Mon”, “Tue”, “Wed”, “Thu”, “Fri”, “Sat”, “Sun”} <br>Dynamic “${data.include_days}” <br>Default: all weekdays - [“Mon”, “Tue”, “Wed”, “Thu”, “Fri”, “Sat”, “Sun”] <br>Enables specific weekdays, for example to enable only working days Monday through Friday and disallow selecting Saturdays and Sundays |
| `min-days _int_` | Dynamic “${data.min_days}” <br>Available only in ‘range’ mode to set the minimum number of days between start and end dates |
| `max-days _int_` | Dynamic “${data.max_days}” <br>Available only in ‘range’ mode to set the maximum number of days between start and end dates |
| `on-select-action _action_` | Only ‘data_exchange’ is supported. <br>Payload that is sent to a data channel business endpoint is a string in “YYYY-MM-DD” format for ‘single’ mode or dictionary in {“start-date”:”YYYY-MM-DD”,”end-date”:”YYYY-MM-DD”} format for ‘range’ mode |
| `init-value _string_` | Dynamic “${data.init-value}” <br>When ‘mode’ is set to ‘range’ the value should be in ‘{“start-date”: String, “end-date”: String}’ format <br>Only available when component is outside Form component |
| `error-message _string_` | Dynamic “${data.error-message}” <br>When ‘mode’ is set to ‘range’ the value should be in ‘{“start-date”: String, “end-date”: String}’ format <br>Only available when component is outside Form component |

### Examples

CalendarPicker single mode example

CalendarPicker range mode example

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Title Max Length | 80 characters |
| Description Max Length | 300 characters |
| Label Max Length | 40 characters |
| Helper Text Max Length | 80 characters |
| Error Message Max Length | 80 characters |

## Image

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “Image” |
| `src _string_`(required) | Base64 of an image. <br>Dynamic “${data.src}” |
| `width _int_` | Dynamic “${data.width}” |
| `height _int_` | Dynamic “${data.height}” |
| `scale-type _string_` | `cover` or `contain`<br>Default value: `contain` |
| `aspect-ratio`Number | Default value: 1 <br>Dynamic “${data.aspect_ratio}” |
| `alt-text _string_` | Alternative Text is for the accessibility feature, eg. Talkback and Voice over <br>Dynamic “${data.alt_text}” |

### Image Scale Types

| Scale Type | Description |
| --- | --- |
| `cover` | Image is clipped to fit the image container.<br>If there is no height value (which is the default), the image will be displayed to its full width with its original aspect ratio.<br>If the height value is set, the image is cropped within the fixed height. Depending on the image whether it is portrait or landscape, image is clipped vertically or horizontally. |
| `contain` | Image is contained within the image container with the original aspect ratio.<br>If there is no height value (which is the default), the image will be displayed to its full width with its original aspect ratio.<br>If the height value is set, the image is contained in the image container with the fixed height and the original aspect ratio.<br>Developers should consider setting a specific height, width and aspect ratio for images whenever using `contain`. On Android devices WhatsApp sets a default height value of 400, which may create some unwanted spacing. |

### Example

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Max number of images per screen<br>Recommended image size<br>Total data channel payload size<br>Supported images formats | 3<br>Up to 300kb<br>1 Mb<br>JPEG<br>PNG |

## If

Supported starting with Flow JSON version 4.0

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “If” |
| `condition _string_`(required) | Boolean expression, it allows both dynamic and static data. Check section below for more info. |
| `then`(required)Array of Components | The components that will be rendered when `condition` is `true`. Allowed components: “TextHeading”, “TextSubheading”, “TextBody”, “TextCaption”, “CheckboxGroup”, “DatePicker”, “Dropdown”, “EmbeddedLink”, “Footer”, “Image”, “OptIn”, “RadioButtonsGroup”, “Switch”, “TextArea”, “TextInput” and “If”*. It is allowed to nest up to 3 “If” components.<br>From V7.1 ChipsSelector is also allowed together with all the previous listed components. |
| `else`Array of Components | The components that will be rendered when `condition` is `false`. Allowed components: “TextHeading”, “TextSubheading”, “TextBody”, “TextCaption”, “CheckboxGroup”, “DatePicker”, “Dropdown”, “EmbeddedLink”, “Footer”, “Image”, “OptIn”, “RadioButtonsGroup”, “Switch”, “TextArea”, “TextInput” and “If”*. It is allowed to nest up to 3 “If” components.<br>From V7.1 ChipsSelector is also allowed together with all the previous listed components. |

### Supported Operators

| Operator | Symbol | Types allowed | Description and examples |
| --- | --- | --- | --- |
| `Parentheses` | `()` | `boolean``number``string` | It is used to define the precedence of operations. Or if you want to perform boolean operations that one of the sides is a result of a number or string comparison. It always require an operation within it. One expression can contain multiple parentheses. Examples:<br>`${form.opt_in} \\|\\| (${data.num_value} > 5)``${form.opt_in} && (${form.address} != '')``!${form.value1}` |
| `Equal to` | `==` | `boolean``number``string` | It is used to compare booleans, numbers and strings. Both sides should have the same type and at least one of them should contain a dynamic variable. Examples:<br>`${form.opt_in} == true``${data.num_value} == 5``${form.city} == 'London'` |
| `Not equal to` | `!=` | `boolean``number``string` | It is used to compare booleans, numbers and strings. Both sides should have the same type and at least one of them should contain a dynamic variable. Examples:<br>`${form.opt_in} != true``${data.num_value} != 5``${form.city} != 'London'` |
| `AND` | `&&` | `boolean` | It performs the boolean `AND` operation. It evaluates as true only if both sides are true. This operator has high priority, i.e. it will be evaluated before other operators. The exception is parentheses, if one of the sides contain an opening or closing parenthesis, then the parenthesis is evaluated first. Example:<br>`${form.opt_in} && ${data.boolean_value}` |
| `OR` | `\|\|` | `boolean` | It performs the boolean `OR` operation. It evaluates as true if at least one side is true. Example:<br>`${form.opt_in} \\|\\| ${data.boolean_value}` |
| `NOT` | `!` | `boolean` | It performs the boolean `NOT` operation. It negates the statement after it. It can be used before immediately `boolean` values or parentheses (that will result into boolean values) Examples:<br>`!(${form.opt_in} \\|\\| ${data.boolean_value})``!(${data.num_value} > 5)``!${form.value1}` |
| `Greater than` | `>` | `number` | It is used to compare to numbers. At least one of them should be a dynamic variable. Examples:<br>`${data.num_value} > 5``${data.num_value} > ${data.num_value2}` |
| `Greater than or equal to` | `>=` | `number` | It is used to compare to numbers. At least one of them should be a dynamic variable. Examples:<br>`${data.num_value} >= 5``${data.num_value} >= ${data.num_value}` |
| `Less than` | `<` | `number` | It is used to compare to numbers. At least one of them should be a dynamic variable. Examples:<br>`${data.num_value} < 5``${data.num_value} < ${data.num_value2}` |
| `Less than or equal to` | `<=` | `number` | It is used to compare to numbers. At least one of them should be a dynamic variable. Examples:<br>`${data.num_value} == 5``${data.num_value} <= ${data.num_value}` |

### Example

### Rules

Condition

- Should have at least one dynamic value (e.g. `${data...}` or `${form...}` ).
- Should always be resolved into a boolean (i.e. no strings or number values).
- Can be used with literals but should not only contain literals.

Footer

- `Footer` can be added within `If` only in the first level, not inside a nested `If` .
- If there is a `Footer` within `If` , it should exist in both branches (i.e. `then` and `else` ). This means that `else` becomes mandatory.
- If there is a `Footer` within `If` it cannot exist a footer outside, because the max count of `Footer` is 1 per screen.

### Limitations and restrictions

The table below show examples of limitations and validation errors that will be shown for certain cases.

| Scenario | Validation error shown |
| --- | --- |
| `Given` there is a footer component inside `then``And` `else` is not defined`When` validating the flow`Then` it should show a validation error | Missing Footer inside one of the if branches. Branch “else” should exist and contain one Footer. |
| `Given` there is a footer component inside `then``And` there is no footer inside `else``When` validating the flow`Then` it should show a validation error | Missing Footer inside one of the if branches. |
| `Given` there is no footer component inside `then``And` there is a footer inside `else``When` validating the flow`Then` it should show a validation error | Missing Footer inside one of the if branches. |
| `Given` there is a footer component inside `then``And` there is a footer component inside `else``And` there is a footer component outside the `If``When` validating the flow`Then` it should show a validation error | You can only have 1 Footer component per screen. |
| `Given` there is an empty array defined for `then``When` validating the flow`Then` it should show a validation error | Invalid value found at: “$root/screens/path_to_your_component/then” due to empty array. It should contain at least one component. |

## Switch

Supported starting with Flow JSON version 4.0

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “Switch” |
| `value _string_`(required) | A variable that will have its value evaluated during runtime. Example<br>`${data.animal}` |
| `cases`(required)Map of Array of Components | Each property is a key (string) that maps to an Array of Components. When the `value` matches the key, it renders its array of components. Allowed components: “TextHeading”, “TextSubheading”, “TextBody”, “TextCaption”, “CheckboxGroup”, “DatePicker”, “Dropdown”, “EmbeddedLink”, “Footer”, “Image”, “OptIn”, “RadioButtonsGroup”, “TextArea”, “TextInput”.<br>From V7.1 ChipsSelector is also allowed together with all the previous listed components. |

### Example

### Rules

Cases

- Should have at least one value. It cannot be empty (e.g. `"cases": {}` )

### Limitations and restrictions

The table below show examples of limitations and validation errors that will be shown for certain cases.

| Scenario | Validation error shown |
| --- | --- |
| `Given` there is a `Switch` component`And` its `cases` property is empty`When` validating the flow`Then` it should show a validation error | Invalid empty property found at: “$root/screens/path_to_your_component/cases”. |

## Media upload

Please refer to the specific page for [media upload components](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/media_upload).

## Navigation List

Supported from Flows v6.2+.

The NavigationList component allows users to navigate effectively between different screens in a Flow, by exploring and interacting with a list of options. Each list item can display rich content such as text, images and tags.

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “NavigationList” |
| `name _string_`(required) |  |
| `list-items`(required)array | Dynamic “${data.list_items}” |
| `label _string_` | Dynamic “${data.label}” |
| `description _string_` | Dynamic “${data.description}” |
| `media-size _enum_` | {‘regular’,’large’} <br>Default: ‘regular’ <br>Dynamic “${data.media-size}” |
| `on-click-action`action | `data_exchange` and `navigate` are supported. |

Each item in the list of items supports the following properties:

| Parameter | Description |
| --- | --- |
| `main-content`(required)object | (required) title <string>description <string>metadata <string> |
| `end`object | title <string>description <string>metadata <string> |
| `start`object | (required) image <base64 encoding of an image>alt-text <string> |
| `badge _string_` |  |
| `tags`Array<string> |  |
| `on-click-action`action | `data_exchange` and `navigate` are supported. |

Images in WEBP format are not supported on iOS versions prior to iOS 14.

The `on-click-action` is required for the component, and it can be defined either:

- Once at component-level and it will apply the same action for all items in the list.
- Individually, on each item in the list to allow for different actions to be triggered.

### Example

### Dynamic Example

In this dynamic example, you can see that `list-items` references the `insurances` of type `array` defined before it using `insurances`. When defining such a structure, you need to specify `items` in the `array`, which will be of type `object`. Then inside the `items` object, you have a `properties` dictionary with `id` and `main-content` just like in the static declaration. Both `id` will always be of type `string` and `main-content` will always be of type `object`, and accompanied by a definition of its structure. Within the `insurances` array, you must define concrete examples in the `__example__` field.

### Limits and Restrictions

- The `Navigation List` component cannot be used on a terminal screen.
- There can be at most 2 `Navigation List` components per screen.
- The `Navigation List` components cannot be used in combination with any other components in the same screen.
- There can be only one item with a `badge` per list.
- The `end` add-on cannot be used in combination with `media-size` set to `large` .
- The `on-click-action` cannot be defined simultaneously on component-level and on item-level.

Component restrictions

| Property | Limit / Restriction |
| --- | --- |
| list-items | minimum 1 and maximum 20 itemsContent will not be rendered if the limit is reached |
| label | 80 charactersContent will truncate if the limit is reached |
| description | 300 charactersContent will truncate if the limit is reached |

List items restrictions

Content over the limit specified will not be rendered.

| Add-on / property | Property | Limit / Restriction |
| --- | --- | --- |
| start | image | 100KBImages over the limit will be replaced by a placeholder |
| main-content | titledescriptionmetadata | 30 characters20 characters80 characters |
| end | titledescriptionmetadata | 10 characters10 characters10 characters |
| badge |  | 15 characters |
| tags |  | 15 characters3 items |

## Chips Selector

Chips Selector component allows users to pick multiple selections from a list of options.

Supported starting with Flow JSON version 6.3

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “ChipsSelector” |
| `data-source _array_`(required) | Dynamic “${data.data_source}”<br>Array< id: String, title: String, enabled: Boolean, on-select-action: {name: 'update_data', payload: {...}}, on-unselect-action: {name: 'update_data', payload: {...}} > |
| `name _string_`(required) |  |
| `min-selected-items _int_` | Dynamic “${data.min_selected_items}” |
| `max-selected-items _int_` | Dynamic “${data.max_selected_items}” |
| `enabled _boolean_` | Dynamic “${data.is_enabled}” |
| `label _string_`(required) | Dynamic “${data.label}” |
| `required _boolean_` | Dynamic “${data.is_required}” |
| `visible _boolean_` | Dynamic “${data.is_visible}” <br>Default: True |
| `description _string_` | Dynamic “${data.description}” |
| `init-value _array<string>` | Dynamic “${data.init-value}” <br>Only available when component is outside Form component |
| `error-message _string_` | Dynamic “${data.error-message}” <br>Only available when component is outside Form component |

If `on-unselect-action` is not added, `on-select-action` will continue to handle both selection and unselection events. However, if `on-unselect-action` is defined, it will exclusively handle unselection, while `on-select-action` will be used solely for selection.

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Label<br>Description<br>Min # of options<br>Max # of options | 80 Characters<br>300 Characters<br>2<br>20 |

### Example

{
"version": "6.3",
"screens": [
{
"id": "DEMO_SCREEN",
"terminal": true,
"title": "Demo screen",
"layout": {
"type": "SingleColumnLayout",
"children": [
{
"type": "ChipsSelector",
"name": "chips",
"label": "Personalize your experience",
"description": "Choose your interests to get personalized design ideas and solution",
"max-selected-items": 2,
"data-source": [
{
"id": "room_layout",
"title": "🏡 Room layouts"
},
{
"id": "lighting",
"title": "💡 Lighting" 
},
{
"id": "renovation",
"title": "🛠️ Renovation"
},
{
"id": "furnitures",
"title": "📐 Room layouts"
}
]
},
{
"type": "Footer",
"label": "Continue",
"on-click-action": {
"name": "complete",
"payload": {}
}
}
]
}
}
]
}

## Image Carousel

The Image Carousel component allows users to slide through multiple images.

Supported from Flows v7.1+.

| Parameter | Description |
| --- | --- |
| `type _string_`(required) | “ImageCarousel” |
| `images`(required)array | Dynamic “${data.images}” |
| `aspect-ratio _string_` | Either “4:3” or “16:9”.<br>Default: “4:3”. |
| `scale-type _string_` | Either “contain” or “cover”.<br>Default: “contain”. |

Each item in the list of images supports the following properties:

| Parameter | Description |
| --- | --- |
| `src _string_`(required) | Base64 of an image. |
| `alt-text _string_`(required) | Alternative text for for accessibility purposes. |

### Limits and Restrictions

| Type | Limit / Restriction |
| --- | --- |
| Min # of images<br>Max # of images<br>Max # of ImageCarousel per screen<br>Max # of ImageCarousel per Flow | 1<br>3<br>2<br>3 |

### Example

{
"version": "7.1",
"screens": [
{
"id": "DEMO_SCREEN",
"terminal": true,
"title": "Demo screen",
"layout": {
"type": "SingleColumnLayout",
"children": [
{
"type": "ImageCarousel",
"scale-type": "cover",
"images": [
{
"alt-text": "Landscape image",
"src": "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAKCAIAAAAsFXl4AAAANElEQVR4nGL5ctWagWjwuH0b8YqZiFdKKhg1Gg2wzOawIV61t1AF8YqHZoAMTaMBAQAA//9ljAXx5eZ2mwAAAABJRU5ErkJggg=="
},
{ 
"alt-text": "Square image",
"src": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAALElEQVR4nGIRPRrBgATeWLsjc5kY8AKaSrPIL3FA5i9evZNudhOQBgQAAP//2DAFw06W30wAAAAASUVORK5CYII="
},
{
"alt-text": "Portrait image",
"src": "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAUCAIAAAA7jDsBAAAALUlEQVR4nGIJWfabAQls8DVA5jIx4AUjVZqRP2AJMn//v6V0s3voSgMCAAD//6kkBrFsdv78AAAAAElFTkSuQmCC"
}
]
},
{
"type": "Footer",
"label": "Continue",
"on-click-action": {
"name": "complete",
"payload": {}
}
}
]
}
}
]
}

## Dynamic components

Here’s a corrected version:

If you check the attribute model of certain components (`Dropdown`, `DatePicker`, `RadioGroup` and `CheckboxGroup`), you will find that some of them accept the `on-xxxx-action` attribute. This attribute allows the component to trigger a data-exchange action. It can be used in the following scenarios:

1. When a user selects a date in the DatePicker component.
2. When the business needs to fetch available data (such as table slots, tickets, etc.) for this selected date by calling a data_exchange action.
3. Once the data is received, the user will see an updated screen with new data.

## Prerequisites

The following steps require communication between the client and the business server. Please ensure that you have configured the data channel before attempting to use this feature.

## Step 1 - Defining the layout

Let’s begin with a minimal example, consisting of an empty form and a CTA button, and gradually add more components.

So, we want to build a simple form that takes a date and displays the list of available time slots. First, we’ll add a `DatePicker` component:

Next step is to add a `Dropdown` where we will display all available timeslots:

## Step 2 - Defining 3P Data

Until now, we’ve been incorporating static mock data, but now we aim to connect a screen with dynamic data. Dynamic data can originate from various sources:

1. Initial message payload
2. `navigate` - transitioning from the previous screen using a `navigate` action
3. `data_exchange` - a request to the business server

In this example, we’ll assume that the data will come from a `data_exchange` request. So, let’s instruct Flow JSON to use the data channel request by providing the `"data_api_version": "3.0"` property.

## Step 3 - Allowing DatePicker to Make a Request to the Server

Let’s provide `"on-select-action"` to the `DatePicker` component so we can execute the call to the business server. In the `payload`, we can pass any data we want to the business server to understand the type of request.

```json
{
   "on-select-action":{
      "name":"data_exchange",
      "payload":{
         "date":"${form.date}",
         "component_action":"update_date"
      }
   }
}
```

In this example, we’ll send the value of the field `date` to the action payload, and we’ll also add some static data `"component_action": "update_date"` to help the server recognize the type of request. There is no strict format here; you can choose whatever works for your case.

Now when you try to select a date, a `data_exchange` request will be executed. The server may return the data that can change the UI. For now, our Flow doesn’t expect or use any data from the server. Let’s fix it by first defining the data model that we expect for a screen.

## Step 4 - Define a Server Data Model

Let’s declare a `data` property for the screen outlining the data that we expect to receive from the server. So, we want to receive an `available_slots` array with timeslot options.

It should have the following model. The `__example__` field is mock data used to display the data within the web preview.

```json
{
    "available_slots": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": { "id": {"type": "string"}, "title": {"type": "string"} }
        },
        "__example__": [ {"id": "1", "title": "08:00"}, {"id": "2", "title": "09:00"} ]
    }
}
```

It means that the expected payload to be returned from server can look like the following:

```json
{
    "version": "3.0",
    "screen": "BOOKING",
    "data": {
       "available_slots": [ {"id": "1", "title": "08:00"}, {"id": "2", "title": "09:00"} ]
    }
}
```

So you Flow JSON now should look like the following:

## Step 5 - Control Visibility of the Component

Now, when we select a date in `DatePicker`, the application will send a request to the business server to get available timeslots. However, we don’t want a `Dropdown` to be visible until there is data to display. How can we hide it?

For this purpose, we can use the `visible` attribute on `Dropdown` and connect it with server data. The business server can control the visibility of the component based on a set condition.

So, we need to make the following changes:

1. Define `is_dropdown_visible` in the `data` model of the screen.
2. Connect a property via dynamic binding `"visible": "${data.is_dropdown_visible}"` .
3. Ensure that the server returns the correct data.

**Let’s update our code:**

*NOTE: The current version of the playground doesn’t support endpoint requests*

## Summary

That’s it! Now you have a dynamic component set up. If you’re facing any challenges, feel free to ask a question on the developer forum. We’ll be happy to help!
