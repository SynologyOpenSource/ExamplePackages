<template>
  <pkg-center-step-content>
    <v-form syno-id="form">
      <v-form-item syno-id="form-item-desc" hide-label textonly>
        The package will be uninstall
      </v-form-item>
    </v-form>
  </pkg-center-step-content>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    ...SYNO.SDS.PkgManApp.Custom.useHook.props,
  },
  setup(props) {
    const { getNext, checkState } = SYNO.SDS.PkgManApp.Custom.useHook(props);
    const headline = 'Notice';

    const getValues = () => {
      return {};
    };

    return {
      getNext,
      checkState,
      headline,
      getValues,
    };
  },
});
</script>
