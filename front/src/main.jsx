import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const Widget = {
	render(self) {
		const intervalId = setInterval(() => {
			const FormPayment_div = document.querySelector('[id="work-area-st8chxvoec3pba7ysqvjelctt51cnem9lbgrihm2"]');
			
			if (FormPayment_div) {
				const div = document.createElement('div');
				const parent = FormPayment_div.parentElement;

				parent.replaceChild(div, FormPayment_div);

				ReactDOM.createRoot(div).render(
					<React.StrictMode>
						<App widget={self} />
					</React.StrictMode>
				);

				clearInterval(intervalId);
			}
		}, 500);
		return true;
	},
	init() {

		return true;
	},
	bind_actions() {
		return true;
	},
	settings() {
		return true;
	},
	onSave() {
    return true;
  },
	destroy() {
    return true;
  },
  advancedSettings(self) {
	this.render(self)
	return true;
  }
};



export default Widget;