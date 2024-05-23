<template>
  <pkg-center-step-content>
    <v-form syno-id="form">
      <v-form-item syno-id="form-item-desc" hide-label textonly>
        {{ removeSettingDesc }}
      </v-form-item>
      <v-form-item syno-id="form-item-radio" hide-label :indent="1">
        <v-radio-group syno-id="radio-group" v-model="radioValue">
          <v-radio syno-id="radio-1" value="backup-option">{{ backupOption }}</v-radio>
          <v-radio syno-id="radio-2" value="remove-option">{{ removeOption }}</v-radio>
        </v-radio-group>
      </v-form-item>
    </v-form>
  </pkg-center-step-content>
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    ...SYNO.SDS.PkgManApp.Custom.useHook.props,
  },
  setup(props) {
    const { getNext, checkState } = SYNO.SDS.PkgManApp.Custom.useHook(props);
    const radioValue = ref('remove-option');
    const headline = 'Uninstall MinimServer';

    const getValues = () => {
      return {
        pkgwizard_backup_option: radioValue.value === 'backup-option',
        pkgwizard_remove_option: radioValue.value === 'remove-option'
      };
    };

    return {
      radioValue,
      getNext,
      checkState,
      headline,
      getValues,
      removeSettingDesc: 'Important information: The uninstallation procedure will completely remove MinimServer from the system. However, you can choose to backup the configuration files. Do you want to...',
      backupOption: '... uninstall MinimServer and backup the configuration files?',
      removeOption: '... remove MinimServer completely?',
    };
  },
});
</script>
