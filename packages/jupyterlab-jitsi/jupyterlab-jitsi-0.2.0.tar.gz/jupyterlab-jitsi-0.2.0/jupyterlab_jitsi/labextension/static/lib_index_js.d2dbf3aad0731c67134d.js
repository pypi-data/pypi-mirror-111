(self["webpackChunkjupyterlab_jitsi"] = self["webpackChunkjupyterlab_jitsi"] || []).push([["lib_index_js"],{

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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jitsi', // API Namespace
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
/* harmony export */   "camIcon": () => (/* binding */ camIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icon.svg */ "./style/icon.svg");








const camIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: 'jupyterlab-jitsi:icon',
    svgstr: _style_icon_svg__WEBPACK_IMPORTED_MODULE_5__.default
});
const SETTINGS_ID = 'jupyterlab-jitsi:plugin';
// interface IJitsiOptions {
// }
class JitsiWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IFrame {
    constructor(options, room_index) {
        super();
        const queryElems = [];
        for (const k in options) {
            if (k === 'options') {
                const opts = options.options;
                const jopts = JSON.stringify(opts);
                queryElems.push(encodeURIComponent(k) + '=' + encodeURIComponent(jopts));
            }
            else {
                queryElems.push(encodeURIComponent(k) + '=' + encodeURIComponent(options[k]));
            }
        }
        this.query = queryElems.join('&');
        const baseUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getBaseUrl();
        this.url = baseUrl + `jitsi/app/index.html?${this.query}`;
        console.log('Full URL: ', this.url);
        let label;
        if ('roomAlias' in options['options']) {
            label = options['options']['roomAlias'];
        }
        else {
            label = `Room #${room_index + 1} ${options['options']['roomName']}`;
        }
        this.id = 'Jitsi';
        this.title.label = label;
        this.title.icon = camIcon;
        this.title.closable = true;
        this.node.style.overflowY = 'auto';
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
    dispose() {
        super.dispose();
    }
    onCloseRequest() {
        this.dispose();
    }
}
/**
 * Initialization data for the jupyterlab-jitsi extension.
 */
const extension = {
    id: 'jupyterlab-jitsi:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    activate: (app, palette, settings, launcher) => {
        let _settings;
        const command = 'jitsi:open';
        let registeredCommands = [];
        const _loadSettings = () => {
            const enpoints = _settings.get('configured_rooms').composite;
            console.log(enpoints);
            // const enpoints = [{"name": "test"}];
            let i = 0;
            for (const c of registeredCommands) {
                c.dispose();
            }
            registeredCommands = [];
            enpoints.forEach((epconf, room_index) => {
                // const full_cmd = command + `:${i}`
                const full_cmd = command + `:${i}`;
                const options = epconf['options'];
                const widget = new JitsiWidget(epconf, room_index);
                let label;
                if ('roomAlias' in options) {
                    label = options['roomAlias'];
                }
                else {
                    label = `Room #${room_index + 1} ${options['roomName']}`;
                }
                const rcmd = app.commands.addCommand(full_cmd, {
                    label: label,
                    execute: () => {
                        if (!widget.isAttached) {
                            // Attach the widget to the main work area if it's not there
                            app.shell.add(widget, 'main');
                        }
                        // Activate the widget
                        app.shell.activateById(widget.id);
                    },
                    icon: camIcon
                });
                registeredCommands.push(rcmd);
                // Add a launcher item if the launcher is available.
                if (launcher) {
                    const lcmd = launcher.add({
                        command: full_cmd,
                        rank: 1 + room_index,
                        category: 'Robotics'
                    });
                    registeredCommands.push(lcmd);
                }
                const pcmd = palette.addItem({
                    command: full_cmd,
                    category: 'Robotics'
                });
                registeredCommands.push(pcmd);
                i += 1;
            });
        };
        settings.load(SETTINGS_ID).then(setting => {
            console.log(setting);
            _settings = setting;
            const extensions = setting.get('configured_endpoints').composite;
            console.log(extensions);
            _loadSettings();
            setting.changed.connect(_loadSettings);
        });
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupyterlab-jitsi server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"48px\" viewBox=\"0 0 24 24\" width=\"48px\" fill=\"#000000\"><path d=\"M0 0h24v24H0V0z\" fill=\"none\"/><path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4zM15 16H5V8h10v8zm-6-1h2v-2h2v-2h-2V9H9v2H7v2h2z\"/></svg>");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.d2dbf3aad0731c67134d.js.map