<template>
  <pkg-center-step-content>
    <v-form syno-id="form">
      <v-form-item syno-id="form-item-desc" hide-label textonly>
        <b>{{ removeSettingDesc }}</b>
      </v-form-item>
      <v-form-item syno-id="form-item-radio" hide-label :indent="1">
        <v-radio-group syno-id="radio-group" v-model="radioValue">
          <v-radio syno-id="radio-1" value="uninstall-option">
            <v-rich-text :text="uninstallOption" />
          </v-radio>
          <v-radio syno-id="radio-2" value="signout-option">
            <v-rich-text :text="signoutOption" />
          </v-radio>
          <v-radio syno-id="radio-3" value="erase-option" label-color="red">
            <v-rich-text :text="eraseOption" />
          </v-radio>
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
    const radioValue = ref('uninstall-option');
    const headline = 'Uninstall Plex Media Server';

    const getValues = () => {
      return {
        pkgwizard_uninstall_option: radioValue.value === 'unintall-option',
        pkgwizard_signout_option: radioValue.value === 'signout-option',
        pkgwizard_erase_option: radioValue.value === 'erase-option'
      };
    };

    return {
      radioValue,
      getNext,
      checkState,
      headline,
      getValues,
      removeSettingDesc: 'Keep or Delete Plex Midia server metadata files.',
      uninstallOption: '<b>Uninstall only.</b> Keep all existing files for future re-installation.',
      signoutOption: '<b>Sign out and unclain this server.</b> Keep all existing files for future re-installation.',
      eraseOption: '<b>Erase all of Plex Midia Server from this system. (Not Recoverable)</b>',
    };
  },
});
</script>
