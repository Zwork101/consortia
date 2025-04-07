const admins = $("#last-of-config");
const adminTemplate = $("#admin-template");
const awards = $("#award-list");
const awardTemplate = $("#semester-template");
const percentages = $("#percentages");
const percentageTemplate = $("#percentage-template");
const thresholds = $("#thresholds");
const thresholdTemplate = $("#threshold-template");

const addAdmin = () => {
	const newAdmin = adminTemplate.clone();
	const lastAdmin = admins.find(".admin-config:last-of-type");
	const lastAdminIndex = parseInt(lastAdmin.find("input[type='email']").attr("name").substring(7));
	const newAdminInput = newAdmin.find("input[type='email']");
	newAdminInput.attr("id", "admins-" + (parseInt(lastAdminIndex) + 1));
	newAdminInput.attr("name", "admins-" + (parseInt(lastAdminIndex) + 1));
	newAdminInput.attr("disabled", false);
	newAdmin.attr("id", "");
	newAdmin.insertAfter(lastAdmin);
	newAdmin.attr("hidden", false);
}

const addAward = () => {
	const newAward = awardTemplate.clone();
	const lastAward = awards.find(".semester-config:last-of-type");
	const lastAwardIndex = parseInt(lastAward.find("input[type='number']").attr("name").split("-")[1]);
	newAward.find("input").toArray().forEach((input) => {
		let oldName = $(input).attr("name")
		let newValue = oldName.split("-");
		newValue[1] = `${lastAwardIndex + 1}`;
		newValue = newValue.join("-");
		newAward.find(`label[for='${oldName}']`).attr("for", newValue);
		$(input).attr("name", newValue);
		$(input).attr("id", newValue);
		$(input).attr("disabled", false);
	})
	newAward.attr("id", "");
	newAward.insertAfter(lastAward);
	newAward.attr("hidden", false);
}

const rmConfig = (btn) => {
	btn.parentNode.remove();
}

const addPercentage = () => {
	const newPercentage = percentageTemplate.clone();
	const lastPercentage = percentages.find(".percentage-config:last-of-type");
	const lastPercentageIndex = parseInt(lastPercentage.find("input[type='number']").attr("name").split("-")[1]);
	newPercentage.find("input").toArray().forEach((input) => {
		let oldName = $(input).attr("name")
		let newValue = $(input).attr("name").split("-");
		newValue[1] = `${lastPercentageIndex + 1}`;
		newValue = newValue.join("-");
		newPercentage.find(`label[for='${oldName}']`).attr("for", newValue);
		$(input).attr("name", newValue);
		$(input).attr("id", newValue);
		$(input).attr("disabled", false);
	})
	newPercentage.attr("id", "");
	newPercentage.insertAfter(lastPercentage);
	newPercentage.attr("hidden", false);
}

const addThreshold = () => {
	const newThreshold = thresholdTemplate.clone();
	const lastThreshold = thresholds.find(".threshold-config:last-of-type");
	const lastThresholdIndex = parseInt(lastThreshold.find("input[type='number']").attr("name").split("-")[1]);
	newThreshold.find("input").toArray().forEach((input) => {
		let oldName = $(input).attr("name")
		let newValue = $(input).attr("name").split("-");
		newValue[1] = `${lastThresholdIndex + 1}`;
		newValue = newValue.join("-");
		newThreshold.find(`label[for='${oldName}']`).attr("for", newValue);
		$(input).attr("name", newValue);
		$(input).attr("id", newValue);
		$(input).attr("disabled", false);
	})
	newThreshold.attr("id", "");
	newThreshold.insertAfter(lastThreshold);
	newThreshold.attr("hidden", false);
}