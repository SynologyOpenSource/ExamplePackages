<template>
  <pkg-center-step-content>
    <v-form syno-id="form">
      <v-form-item syno-id="form-item-desc" hide-label textonly>
        <b>Installation Type</b>
      </v-form-item>
      <v-form-item syno-id="form-item-radio" hide-label :indent="1">
        <v-radio-group syno-id="radio-group" v-model="radioValue">
          <v-radio syno-id="radio-1" value="normal-option">Normal installation</v-radio>
          <v-radio syno-id="radio-2" value="token-option">
            <v-rich-text :text="tokenOption" />
          </v-radio>
        </v-radio-group>
      </v-form-item>
      <v-form-item syno-id="form-item-desc2" hide-label textonly>
        <v-rich-text :text="claimTokenDesc" :allow-attrs="['href']" />
      </v-form-item>
      <v-form-item syno-id="form-item-input" label="Claim Token::" label-flex="120px" control-flex="250px" :indent="1">
        <v-input syno-id="input" v-model="claimToken" />
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
    const radioValue = ref('noraml-option');
    const claimToken = ref(null);
    const headline = 'Plex Media Server - Installation options';

    const getValues = () => {
      return {
        pkgwizard_noramal_option: radioValue.value === 'normal-option',
        pkgwizard_token_option: radioValue.value === 'token-option',
        pkgwizard_claim_token: claimToken.value
      };
    };

    return {
      radioValue,
      getNext,
      checkState,
      headline,
      getValues,
      tokenOption: 'Install using Plex Claim Token<br/><span style="color: red; font-style: italic;">New or lost servers only</span>',
      claimTokenDesc: 'Claim Token string from <a href="https://help.synology.com/developer-guide" style="color: #057FEB; font-weight: bold;">Get Plex Claim Token</a><br><span style="font-style: italic;">Leave blank if not used</span>'
    };
  },
});
</script>
  