const STRINGS = __STRINGS__;
export function $t(lang, section, key) {
	return STRINGS?.[lang]?.[section]?.[key];
}
