const STRINGS = __STRINGS__;
export function $t(lang, section, key) {
	let langStrings = STRINGS?.[lang];
	if (!langStrings) {
		langStrings = STRINGS?.['enu'];
	}
	return langStrings?.[section]?.[key];
}
