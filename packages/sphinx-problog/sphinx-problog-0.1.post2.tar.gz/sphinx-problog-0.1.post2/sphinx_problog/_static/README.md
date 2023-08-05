# Static Dependencies and Requirements #
The `sphinx-problog` extension uses a collection of  `css` and `js` files,
some of which are loaded from various CDNs.

## CDN Requirements ##
These files are loaded by the `sphinx_problog.problog` Python module, which
lists them under the `DEPENDENCIES` variable. These are:

- [CryptoJS] (MIT),
- [jQuery] (MIT) and
- [jQuery UI] (MIT).

[Ace]: https://github.com/ajaxorg/ace
[CryptoJS]: https://github.com/brix/crypto-js
[jQuery]: https://github.com/jquery/jquery
[jQuery UI]: https://github.com/jquery/jquery-ui

## Local Requirements ##
Additionally, `sphinx-problog` requires [`ace.js`](ace.js) version
[1.1.3](https://cdnjs.cloudflare.com/ajax/libs/ace//ace.js) --
[Ajax.org Cloud9 Editor (BSD)](https://github.com/ajaxorg/ace) --
and two ProbLog-specific files:

- `mode-problog.js` and
- `problog_editor_advanced.js`.

These are distributed under the *Apache V2 License* (see below)
and were copied from the [ProbLog repository] (version 2.1.0.13.dev2).

> Copyright 2015 KU Leuven, DTAI Research Group
>
> Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

[ProbLog repository]: https://github.com/ML-KULeuven/problog/tree/master/problog/web/js
