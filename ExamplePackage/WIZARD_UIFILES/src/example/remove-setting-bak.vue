<template>
	<pkg-center-step-content>
		<v-form syno-id="form">
			<v-form-item syno-id="form-item" hide-label>
				<v-checkbox v-model="removeSetting" syno-id="checkbox">
					{{ removeSettingDesc }}
				</v-checkbox>
			</v-form-item>
		</v-form>
	</pkg-center-step-content>
</template>

<script>
import { $t } from './utils/uistring';
import { defineComponent, ref } from 'vue';

export default defineComponent({
	props: {
		...SYNO.SDS.PkgManApp.Custom.useHook.props,
	},
	setup(props) {
		const { getNext, checkState } = SYNO.SDS.PkgManApp.Custom.useHook(props);

		const removeSetting = ref(false);
		const headline = $t(_S('lang'), 'wizard', 'remove_setting_title');

		const getValues = () => {
			return {
				pkgwizard_remove_setting: removeSetting.value,
			};
		};

		return {
			removeSetting,
			getNext,
			checkState,
			headline,
			getValues,
			removeSettingDesc: $t(_S('lang'), 'wizard', 'remove_setting_desc'),
		};
	},
});
</script>
