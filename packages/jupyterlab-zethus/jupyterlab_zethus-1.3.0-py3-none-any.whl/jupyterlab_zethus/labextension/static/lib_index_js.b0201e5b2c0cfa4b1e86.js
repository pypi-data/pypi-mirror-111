(self["webpackChunkjupyterlab_zethus"] = self["webpackChunkjupyterlab_zethus"] || []).push([["lib_index_js"],{

/***/ "./lib/default_config.js":
/*!*******************************!*\
  !*** ./lib/default_config.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default_config": () => (/* binding */ default_config)
/* harmony export */ });
const default_config = (defaultROSEndpoint, defaultROSPKGSEndpoint) => {
    return `{
        "panels": {
          "sidebar": {
            "display": true,
            "collapsed": false
          },
          "header": {
            "display": true
          },
          "info": {
            "display": true,
            "collapsed": true
          }
        },
        "ros": {
          "endpoint": "${defaultROSEndpoint}",
          "pkgsEndpoint": "${defaultROSPKGSEndpoint}"
        },
        "infoTabs": [],
        "visualizations": [],
        "globalOptions": {
          "display": true,
          "backgroundColor": {
            "display": true,
            "value": 15790320
          },
          "fixedFrame": {
            "display": true,
            "value": "world"
          },
          "grid": {
            "display": true,
            "size": 30,
            "divisions": 30,
            "color": 11184810,
            "centerlineColor": 7368816
          }
        },
        "tools": {
          "mode": "controls",
          "controls": {
            "display": false,
            "enabled": true
          },
          "measure": {
            "display": false
          },
          "custom": []
        }
      }`;
};


/***/ }),

/***/ "./lib/editor.js":
/*!***********************!*\
  !*** ./lib/editor.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ZethusWidget": () => (/* binding */ ZethusWidget),
/* harmony export */   "ZethusFactory": () => (/* binding */ ZethusFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _default_config__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./default_config */ "./lib/default_config.js");
// Copyright 2018 Wolf Vollprecht
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.






let zethusEditorId = 0;
class ZethusWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget {
    constructor(options, defaultROSEndpoint, defaultROSPKGSEndpoint) {
        super(Object.assign({}, options));
        this.countSetConfig = 0;
        // private _editor : any;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.title.icon = _icons__WEBPACK_IMPORTED_MODULE_4__.zethusIcon;
        zethusEditorId += 1;
        this.zethusId = zethusEditorId;
        this.context = options['context'];
        this._onTitleChanged();
        this.context.pathChanged.connect(this._onTitleChanged, this);
        this.context.ready.then(() => {
            this._onContextReady();
        });
        this._defaultROSEndpoint = defaultROSEndpoint;
        this._defaultROSPKGSEndpoint = defaultROSPKGSEndpoint;
        // this.context.ready.then(() => { this._handleDirtyStateNew(); });
        window.onmessage = (event) => {
            if (event.data && event.data === 'save') {
                event.preventDefault();
                this.context.save();
            }
        };
    }
    loadEditor(state) {
        var _a;
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl();
        if (!this.iframe) {
            this.iframe = document.createElement('iframe');
            this.iframe.className = 'jp-iframe-zethus';
            const q = encodeURIComponent(JSON.stringify(state));
            this.iframe.src =
                baseUrl +
                    `zethus/app/index.html?config=${q}&zethusId=${this.zethusId}&bridge=${this._defaultROSEndpoint}&pkgs=${this._defaultROSPKGSEndpoint}`;
            this.content.node.appendChild(this.iframe);
            window.document.addEventListener(`ZethusUpdateConfig${this.zethusId}`, (e) => {
                if (this.countSetConfig <= 0) {
                    this._saveToContext(e.detail.config);
                }
                else {
                    this.countSetConfig--;
                }
            }, false);
        }
        else {
            this.countSetConfig++;
            const event = new CustomEvent('SetConfig', { detail: { config: state } });
            (_a = this.iframe.contentDocument) === null || _a === void 0 ? void 0 : _a.dispatchEvent(event);
        }
    }
    // protected onResize(msg: Widget.ResizeMessage): void {}
    _onContextReady() {
        const contextModel = this.context.model;
        if (this.context.model.toString() === '') {
            this.context.model.fromString((0,_default_config__WEBPACK_IMPORTED_MODULE_5__.default_config)(this._defaultROSEndpoint, this._defaultROSPKGSEndpoint));
        }
        // Set the editor model value.
        this._onContentChanged();
        contextModel.contentChanged.connect(this._onContentChanged, this);
        this._ready.resolve(void 0);
    }
    /**
     * Handle a change to the title.
     */
    _onTitleChanged() {
        this.title.label = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.basename(this.context.localPath);
    }
    _onContentChanged() {
        try {
            const editor_value = this.context.model.toString();
            const state = JSON.parse(editor_value);
            console.log('Loading editor from content changed!');
            this.loadEditor(state);
        }
        catch (e) {
            // maybe empty string/
        }
    }
    _saveToContext(content) {
        console.log('Saving content: ', content);
        this.context.ready.then(() => {
            this.context.model.fromString(JSON.stringify(content, null, 4));
        });
    }
    // private _onModelStateChangedNew(sender: DocumentRegistry.IModel, args: IChangedArgs<any>): void {
    //     // if (args.name === 'dirty') {
    //     //     this._handleDirtyStateNew();
    //     // }
    // }
    // private _handleDirtyStateNew() : void {
    //     // if (this.context.model.dirty) {
    //     //     this.title.className += ` ${DIRTY_CLASS}`;
    //     // } else {
    //     //     this.title.className = this.title.className.replace(DIRTY_CLASS, '');
    //     // }
    // }
    onBeforeDetach(msg) {
        // ReactDOM.unmountComponentAtNode(this.node);
    }
    /**
     * A promise that resolves when the zethus viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
}
/**
 * A widget factory for drawio.
 */
class ZethusFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    constructor(options, defaultROSEndpoint, defaultROSPKGSEndpoint) {
        super(options);
        this.defaultROSEndpoint = defaultROSEndpoint;
        this.defaultROSPKGSEndpoint = defaultROSPKGSEndpoint;
    }
    createNewWidget(context) {
        return new ZethusWidget({ context, content: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget() }, this.defaultROSEndpoint, this.defaultROSPKGSEndpoint);
    }
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "zethusIcon": () => (/* binding */ zethusIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icon_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg");
// Copyright 2018 Wolf Vollprecht
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


const zethusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'jupyterlab-zethus:icon',
    svgstr: _style_icon_svg__WEBPACK_IMPORTED_MODULE_1__.default
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IZethusTracker": () => (/* binding */ IZethusTracker),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./editor */ "./lib/editor.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
// Copyright 2018 Wolf Vollprecht
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.










/**
 * The name of the factory that creates editor widgets.
 */
const FACTORY = 'Zethus';
const IZethusTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.Token('zethus/tracki');
/**
 * The editor tracker extension.
 */
const plugin = {
    activate,
    id: 'jupyterlab-zethus:plugin',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    provides: IZethusTracker,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
// function activate(
//   app: JupyterFrontEnd,
//   browserFactory: IFileBrowserFactory,
//   restorer: ILayoutRestorer,
//   menu: IMainMenu,
//   palette: ICommandPalette,
//   launcher: ILauncher | null
// ): IDrawioTracker {
function activate(app, browserFactory, restorer, settingRegistry, launcher) {
    const namespace = 'zethus';
    const { commands } = app;
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
    let defaultROSEndpoint = '';
    let defaultROSPKGSEndpoint = '';
    const factory = new _editor__WEBPACK_IMPORTED_MODULE_8__.ZethusFactory({
        name: FACTORY,
        fileTypes: ['zethus'],
        defaultFor: ['zethus']
    }, defaultROSEndpoint, defaultROSPKGSEndpoint);
    const updateSettings = (settings) => {
        defaultROSEndpoint = settings.get('defaultROSEndpoint').composite;
        defaultROSPKGSEndpoint = settings.get('defaultROSPKGSEndpoint')
            .composite;
        console.log(`Updating ROS Endpoint to --> ${defaultROSEndpoint}, ${defaultROSPKGSEndpoint}`);
        factory.defaultROSEndpoint = defaultROSEndpoint;
        factory.defaultROSPKGSEndpoint = defaultROSPKGSEndpoint;
    };
    Promise.all([
        settingRegistry.load('jupyterlab-zethus:settings'),
        app.restored
    ])
        .then(([settings]) => {
        updateSettings(settings);
        settings.changed.connect(updateSettings);
    })
        .catch((reason) => {
        console.error(reason.message);
    });
    /**
     * Whether there is an active Zethus viewer.
     */
    function isEnabled() {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === app.shell.currentWidget);
    }
    const zethusCSSSelector = '.jp-DirListing-item[title$=".zethus"]';
    app.contextMenu.addItem({
        command: 'zethus:launch-simulation',
        selector: zethusCSSSelector,
        rank: 1
    });
    // Handle state restoration.
    restorer.restore(tracker, {
        command: 'docmanager:open',
        args: widget => ({ path: widget.context.path, factory: FACTORY }),
        name: widget => widget.context.path
    });
    factory.widgetCreated.connect((sender, widget) => {
        // Notify the instance tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            tracker.save(widget);
        });
        tracker.add(widget);
    });
    app.docRegistry.addWidgetFactory(factory);
    // Function to create a new untitled diagram file, given
    // the current working directory.
    const createNewZethus = (cwd) => {
        return commands
            .execute('docmanager:new-untitled', {
            path: cwd,
            type: 'file',
            ext: '.zethus'
        })
            .then(model => {
            return commands.execute('docmanager:open', {
                path: model.path,
                factory: FACTORY
            });
        });
    };
    app.docRegistry.addFileType({
        name: 'zethus',
        displayName: 'Zethus File',
        mimeTypes: ['application/json'],
        extensions: ['.zethus'],
        icon: _icons__WEBPACK_IMPORTED_MODULE_9__.zethusIcon,
        fileFormat: 'text'
    });
    app.docRegistry.addFileType({
        name: 'roslaunch',
        displayName: 'ROS Launch File',
        mimeTypes: ['application/xml'],
        extensions: ['.launch'],
        icon: _icons__WEBPACK_IMPORTED_MODULE_9__.zethusIcon,
        fileFormat: 'text'
    });
    commands.addCommand('zethus:launch', {
        label: 'Zethus',
        icon: _icons__WEBPACK_IMPORTED_MODULE_9__.zethusIcon,
        caption: 'Launch the Zethus viewer',
        execute: () => {
            const cwd = browserFactory.defaultBrowser.model.path;
            return createNewZethus(cwd);
        },
        isEnabled
    });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            command: 'zethus:launch',
            rank: 1,
            category: 'Robotics'
        });
    }
    _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_6__.Mode.getModeInfo().push({
        name: 'ROS Launch',
        mime: 'application/xml',
        mode: 'xml',
        ext: ['launch']
    });
    _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_6__.Mode.getModeInfo().push({
        name: 'Zethus',
        mime: 'application/json',
        mode: 'json',
        ext: ['zethus']
    });
    return tracker;
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ (() => {

throw new Error("Module build failed (from ./node_modules/css-loader/dist/cjs.js):\nCssSyntaxError\n\n(9:8) /Users/wolfvollprecht/Programs/jupyterlab-zethus/style/base.css Unknown word\n\n \u001b[90m  7 | \u001b[39m    height\u001b[33m:\u001b[39m 100%\u001b[33m;\u001b[39m\n \u001b[90m  8 | \u001b[39m    border\u001b[33m:\u001b[39m none\u001b[33m;\u001b[39m\n\u001b[1m\u001b[31m>\u001b[39m\u001b[22m\u001b[90m  9 | \u001b[39m    // zethus only works well with a white background right now\n \u001b[90m    | \u001b[39m       \u001b[1m\u001b[31m^\u001b[39m\u001b[22m\n \u001b[90m 10 | \u001b[39m    background\u001b[33m:\u001b[39m \u001b[35m#FFF\u001b[39m\u001b[33m;\u001b[39m\n \u001b[90m 11 | \u001b[39m\u001b[33m}\u001b[39m\n");

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__.default);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/icon.svg":
/*!************************!*\
  !*** ./style/icon.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"120\" height=\"120\" viewBox=\"0 0 120 120\"><path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M27.87475805 65.8655666l14.3661193 24.88603303L56.60900197 65.8655666zM68.87956088 44.61116983L59.9999997 29.23236345H6.72263264l8.87956118 15.37880638zM92.12524136 54.13443904l-14.3661193-24.8840277-14.36812462 24.8840277zM51.12043853 75.38883581L59.9999997 90.7676422h53.27736707l-8.87956118-15.37880638z\"/></svg>");

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.b0201e5b2c0cfa4b1e86.js.map