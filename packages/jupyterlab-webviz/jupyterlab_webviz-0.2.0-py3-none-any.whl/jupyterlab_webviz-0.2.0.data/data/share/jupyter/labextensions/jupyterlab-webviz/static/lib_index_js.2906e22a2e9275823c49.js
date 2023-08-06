(self["webpackChunkjupyterlab_webviz"] = self["webpackChunkjupyterlab_webviz"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'webviz', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "webvizIcon": () => (/* binding */ webvizIcon),
/* harmony export */   "WebvizWidget": () => (/* binding */ WebvizWidget),
/* harmony export */   "WebvizFactory": () => (/* binding */ WebvizFactory),
/* harmony export */   "IWebvizTracker": () => (/* binding */ IWebvizTracker),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _style_logo_svg__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/logo.svg */ "./style/logo.svg");


// import { Widget } from '@lumino/widgets';











const webvizIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
    name: 'jupyterlab-webviz:icon',
    svgstr: _style_logo_svg__WEBPACK_IMPORTED_MODULE_9__.default
});
class WebvizIframeWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.IFrame {
    constructor(webvizOptions) {
        super();
        this.query = '';
        // const queryElems = [];
        // for (const k in webvizOptions as any) {
        //   let kk = k;
        //   kk.replace(/[A-Z]/g, (letter: string) => `-${letter.toLowerCase()}`);
        //   queryElems.push(
        //     encodeURIComponent(kk) + '=' + encodeURIComponent((webvizOptions as any)[k])
        //   );
        // }
        // this.query = queryElems.join('&');
        // const baseUrl = PageConfig.getBaseUrl();
        // this.url = baseUrl + `webviz/app/index.html?${this.query}`;
        this.id = 'Webviz ABABABA';
        this.title.label = 'Webviz ABABABA';
        this.title.closable = true;
        this.title.icon = webvizIcon;
        this.node.style.overflowY = 'hidden';
        this.node.style.background = '#FFF';
        this.sandbox = [
            'allow-forms',
            'allow-modals',
            'allow-orientation-lock',
            'allow-pointer-lock',
            'allow-popups',
            'allow-presentation',
            'allow-same-origin',
            'allow-scripts',
            'allow-top-navigation',
            'allow-top-navigation-by-user-activation'
        ];
    }
    trigger(webvizOptions) {
        const queryElems = [];
        for (const k in webvizOptions) {
            const kk = k.replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`);
            queryElems.push(encodeURIComponent(kk) +
                '=' +
                encodeURIComponent(webvizOptions[k]));
        }
        this.query = queryElems.join('&');
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__.PageConfig.getBaseUrl();
        this.url = baseUrl + `webviz/app/index.html?${this.query}`;
        console.log('Full URL: ', this.url);
    }
    dispose() {
        super.dispose();
    }
    onCloseRequest() {
        this.dispose();
    }
}
class WebvizWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    constructor(options, defaultROSEndpoint) {
        super(Object.assign({}, options));
        this.defaultROSEndpoint = '';
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__.PromiseDelegate();
        this.defaultROSEndpoint = defaultROSEndpoint;
        this.context.ready.then(() => {
            this._onContextReady();
        });
        // this.context.ready.then(() => { this._handleDirtyStateNew(); });
    }
    _onContentChanged() {
        console.log('Content changed?');
    }
    /**
     * A promise that resolves when the zethus viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    _onContextReady() {
        const contextModel = this.context.model;
        // if (contextModel.toString() === '') {
        // contextModel.fromString();
        // }
        // Set the editor model value.
        // this._onContentChanged();
        contextModel.contentChanged.connect(this._onContentChanged, this);
        let layout = {};
        try {
            layout = JSON.parse(this.context.model.toString());
        }
        catch (e) {
            // ignore
        }
        this.content.trigger({
            rosbridgeWebsocketUrl: this.defaultROSEndpoint,
            layout: JSON.stringify(layout)
        });
        // let widget = new WebvizIframeWidget({});
        // console.log(widget)
        // this.content.addChild(widget);
        this._ready.resolve(void 0);
    }
}
/**
 * A widget factory for drawio.
 */
class WebvizFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    constructor(options, defaultROSEndpoint) {
        super(options);
        this.defaultROSEndpoint = defaultROSEndpoint;
    }
    createNewWidget(context) {
        return new WebvizWidget({ context, content: new WebvizIframeWidget({}) }, this.defaultROSEndpoint);
    }
}
const IWebvizTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__.Token('webviz/track');
/**
 * The name of the factory that creates editor widgets.
 */
const FACTORY = 'WebvizFactory';
/**
 * Initialization data for the jupyterlab-webviz extension.
 */
const plugin = {
    id: 'jupyterlab-webviz:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__.ISettingRegistry, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher],
    activate: async (app, browserFactory, restorer, settingRegistry, launcher) => {
        console.log('JupyterLab extension jupyterlab-webviz is activated!');
        let defaultROSEndpoint = 'ws://localhost:9090';
        if (settingRegistry) {
            const settings = await settingRegistry.load(plugin.id);
            defaultROSEndpoint = settings.get('defaultROSEndpoint')
                .composite;
            console.log('jupyterlab-webviz settings loaded:', settings.composite);
        }
        const namespace = 'jupyterlab-webviz';
        const { commands } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.WidgetTracker({ namespace });
        const factory = new WebvizFactory({ name: FACTORY, fileTypes: ['webviz'], defaultFor: ['webviz'] }, defaultROSEndpoint);
        // Handle state restoration.
        restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY }),
            name: widget => widget.context.path
        });
        factory.widgetCreated.connect((sender, widget) => {
            widget.title.icon = 'jp-MaterialIcon ZethusIcon'; // TODO change
            // Notify the instance tracker if restore data needs to update.
            widget.context.pathChanged.connect(() => {
                tracker.save(widget);
            });
            tracker.add(widget);
        });
        app.docRegistry.addWidgetFactory(factory);
        // Function to create a new untitled diagram file, given
        // the current working directory.
        const createNewWebviz = (cwd) => {
            return commands
                .execute('docmanager:new-untitled', {
                path: cwd,
                type: 'file',
                ext: '.webviz'
            })
                .then(model => {
                return commands.execute('docmanager:open', {
                    path: model.path,
                    factory: FACTORY
                });
            });
        };
        app.docRegistry.addFileType({
            name: 'webviz',
            displayName: 'Webviz File',
            mimeTypes: ['application/json'],
            extensions: ['.webviz'],
            icon: webvizIcon,
            fileFormat: 'text'
        });
        commands.addCommand('webviz:launch', {
            label: 'Webviz',
            icon: webvizIcon,
            caption: 'Launch the Webviz viewer',
            execute: () => {
                const cwd = browserFactory.defaultBrowser.model.path;
                return createNewWebviz(cwd);
            }
            // isEnabled
        });
        // app.commands.addCommand("webviz:open", {
        //   label: 'Webviz',
        //   icon: webvizIcon,
        //   execute: () => {
        //     let widget = new WebvizWidget({}, defaultROSEndpoint);
        //     app.shell.add(widget, 'main');
        //     // Activate the widget
        //     app.shell.activateById(widget.id);
        //   },
        // });
        // Add a launcher item if the launcher is available.
        if (launcher) {
            launcher.add({
                command: 'webviz:launch',
                rank: 5,
                category: 'Robotics'
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_10__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab-webviz server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./style/logo.svg":
/*!************************!*\
  !*** ./style/logo.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<!--\nCopyright (c) 2018-present, GM Cruise LLC\n\nThis source code is licensed under the Apache License, Version 2.0,\nfound in the LICENSE file in the root directory of this source tree.\nYou may not use this file except in compliance with the License.\n-->\n<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"28\" height=\"28\" viewBox=\"0 0 28 28\">\n  <title>\n    webviz\n  </title>\n  <desc>\n    webviz logo\n  </desc>\n  <g fill=\"none\" fill-rule=\"evenodd\" stroke-width=\"2\">\n    <path stroke=\"#E987FF\" d=\"M11 2.8v14.116l11.29 4.168V5.996L11 2z\" opacity=\".983\"/>\n    <path fill=\"#20C0FF\" fill-opacity=\".3\" fill-rule=\"nonzero\" stroke=\"#20C0FF\" d=\"M8 4.8v14.116l11.29 4.168V7.996L8 4z\"/>\n    <path stroke=\"#BD10E0\" d=\"M5 6.8v14.116l11.29 4.168V9.996L5 6z\"/>\n  </g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.2906e22a2e9275823c49.js.map