/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/scripts/components/add-remove.js":
/*!**********************************************!*\
  !*** ./src/scripts/components/add-remove.js ***!
  \**********************************************/
/***/ (() => {

eval("// Add remove rows on recipe forms\ndocument.addEventListener('click', function (e) {\n  if (!e.target.closest('.btn-add-remove')) return;\n  var isAdd = e.target.closest('.btn-add-remove__input--add');\n  var isRemove = e.target.closest('.btn-add-remove__input--remove');\n  var targetBtns = e.target.closest('.btn-add-remove');\n  var targetRow = e.target.closest('.form__row');\n  var targetInputs = targetRow.querySelectorAll('.form__inputs');\n  var targetInputsNum = targetInputs.length;\n\n  if (isAdd !== null) {\n    var cloneInput = targetInputs[0].cloneNode(true);\n    cloneInput.classList.remove(\"hide\");\n    targetRow.insertBefore(cloneInput, targetBtns);\n  }\n\n  if (isRemove !== null) {\n    if (targetRow.querySelectorAll('.form__inputs').length > 2) {\n      var cloneInputRemove = targetInputs[targetInputsNum - 1];\n      cloneInputRemove.parentNode.removeChild(cloneInputRemove);\n    }\n  }\n});\n\n//# sourceURL=webpack://crockpot/./src/scripts/components/add-remove.js?");

/***/ }),

/***/ "./src/scripts/components/modal.js":
/*!*****************************************!*\
  !*** ./src/scripts/components/modal.js ***!
  \*****************************************/
/***/ (() => {

eval("// Open/close modal\ndocument.addEventListener('click', function (e) {\n  if (!e.target.closest('.modal__buttons')) return; // console.log(e.target)\n\n  var modalIdentifier = e.target.closest('.modal__buttons').classList[1].split(\"--\")[1];\n  var modal = document.querySelector(\".modal--\".concat(modalIdentifier));\n  var isOpen = document.querySelector(\".modal__button--open--\".concat(modalIdentifier));\n  var isClose = e.target.closest(\".modal__button--close--\".concat(modalIdentifier)); // console.log(modalIdentifier, modal, isOpen, isClose)\n\n  if (isOpen !== null) {\n    modal.classList.remove(\"hide\");\n  }\n\n  if (isClose !== null) {\n    modal.classList.add(\"hide\");\n  }\n});\n\n//# sourceURL=webpack://crockpot/./src/scripts/components/modal.js?");

/***/ }),

/***/ "./src/scripts/components/plus-minus.js":
/*!**********************************************!*\
  !*** ./src/scripts/components/plus-minus.js ***!
  \**********************************************/
/***/ (() => {

eval("// Plus minus button\ndocument.addEventListener('click', function (e) {\n  if (!e.target.closest('.btn-plus-minus__input')) return;\n  var num = e.target.closest('.btn-plus-minus__btn').querySelector('.btn-plus-minus__num');\n  var numVal = parseInt(num.value);\n  var minVal = num.getAttribute(\"min\");\n  var maxVal = num.getAttribute(\"max\");\n  var step = parseInt(num.getAttribute(\"step\"));\n  var stepUp = true;\n  var isPlus = e.target.closest('.btn-plus-minus__input--plus');\n  var isMinus = e.target.closest('.btn-plus-minus__input--minus');\n  var isViewRecipe = e.target.closest('.view-recipe');\n  var isEditRecipe = e.target.closest('.edit-recipe');\n\n  if (isPlus !== null && numVal < maxVal) {\n    numVal += step;\n    stepUp = true;\n  }\n\n  if (isMinus !== null && numVal > minVal) {\n    numVal -= step;\n    stepUp = false;\n  }\n\n  num.value = numVal;\n\n  if (isEditRecipe !== null) {\n    multiplyInputs(numVal, stepUp);\n  }\n\n  if (isViewRecipe !== null) {\n    multiplyIngs(numVal);\n  }\n}); // If on the same page as edit recipe, change quantity of ingredient inputs\n\nfunction multiplyInputs(numVal, stepUp) {\n  var targetInputs = document.querySelectorAll('.btn-plus-minus__targetInput');\n\n  for (var i = 0; i < targetInputs.length; i++) {\n    var targetInput = parseFloat(targetInputs[i].value);\n    console.log(stepUp);\n\n    if (numVal > 1 && stepUp == true) {\n      var targetInputSingle = targetInput / (numVal - 1);\n    } else if (numVal >= 1 && stepUp == false) {\n      var targetInputSingle = targetInput / (numVal + 1);\n    } else {\n      var targetInputSingle = targetInput / numVal;\n    }\n\n    targetInputs[i].value = targetInputSingle * numVal;\n  }\n} // If on the same page as view recipe, change quantity of ingredients\n\n\nfunction multiplyIngs(numVal) {\n  var targetNums = document.querySelectorAll('.btn-plus-minus__targetNum');\n  var targetNumsHidden = document.querySelectorAll('.btn-plus-minus__targetNum--hidden');\n  var ingNums = document.querySelectorAll('.btn-plus-minus__ingNum');\n\n  for (var i = 0; i < targetNums.length; i++) {\n    var targetNum = targetNums[i];\n    var targetNumHidden = targetNumsHidden[i];\n    var ingNum = parseFloat(ingNums[i].innerHTML);\n    var ingNumHidden = parseFloat(targetNumHidden.innerHTML);\n    var targetNumNew = ingNum * numVal;\n\n    if (String(ingNumHidden).includes('.')) {\n      targetNum.innerHTML = targetNumNew.toFixed(2);\n\n      if (targetNum.innerHTML.includes('.')) {\n        if (targetNum.innerHTML.includes('.00')) {\n          targetNum.innerHTML -= \".00\";\n        }\n\n        if (targetNum.innerHTML.slice(-1) == \"0\") {\n          targetNum.innerHTML -= \"0\";\n        }\n      }\n    } else {\n      targetNum.innerHTML = targetNumNew;\n    }\n  }\n}\n\n//# sourceURL=webpack://crockpot/./src/scripts/components/plus-minus.js?");

/***/ }),

/***/ "./src/scripts/components/toggle.js":
/*!******************************************!*\
  !*** ./src/scripts/components/toggle.js ***!
  \******************************************/
/***/ (() => {

eval("// Toggle switch\ndocument.addEventListener('click', function (e) {\n  if (!e.target.closest('.toggle__input')) return;\n  var slider = e.target.closest('.toggle').querySelector('.toggle__slider');\n  var isToggleBox = e.target.closest('.toggle-box__container');\n\n  if (e.target.classList.contains('toggle__input--1')) {\n    slider.style.transform = \"translate(0%,0)\"; // If component is toggleBox show/hide content\n\n    if (isToggleBox !== null) {\n      isToggleBox.querySelector('.toggle-box__box-left').classList.remove(\"hide\");\n      isToggleBox.querySelector('.toggle-box__box-right').classList.add(\"hide\");\n    }\n  }\n\n  if (e.target.classList.contains('toggle__input--2')) {\n    slider.style.transform = \"translate(100%,0)\"; // If component is toggleBox show/hide content\n\n    if (isToggleBox !== null) {\n      isToggleBox.querySelector('.toggle-box__box-left').classList.add(\"hide\");\n      isToggleBox.querySelector('.toggle-box__box-right').classList.remove(\"hide\");\n    }\n  }\n});\n\n//# sourceURL=webpack://crockpot/./src/scripts/components/toggle.js?");

/***/ }),

/***/ "./src/scripts/index.js":
/*!******************************!*\
  !*** ./src/scripts/index.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _styles_style_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../styles/style.scss */ \"./src/styles/style.scss\");\n/* harmony import */ var _components_add_remove__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./components/add-remove */ \"./src/scripts/components/add-remove.js\");\n/* harmony import */ var _components_add_remove__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_components_add_remove__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _components_modal__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./components/modal */ \"./src/scripts/components/modal.js\");\n/* harmony import */ var _components_modal__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_components_modal__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _components_plus_minus__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/plus-minus */ \"./src/scripts/components/plus-minus.js\");\n/* harmony import */ var _components_plus_minus__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_components_plus_minus__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _components_toggle__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/toggle */ \"./src/scripts/components/toggle.js\");\n/* harmony import */ var _components_toggle__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_components_toggle__WEBPACK_IMPORTED_MODULE_4__);\n\n\n\n\n\n\n//# sourceURL=webpack://crockpot/./src/scripts/index.js?");

/***/ }),

/***/ "./src/styles/style.scss":
/*!*******************************!*\
  !*** ./src/styles/style.scss ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://crockpot/./src/styles/style.scss?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/scripts/index.js");
/******/ 	
/******/ })()
;