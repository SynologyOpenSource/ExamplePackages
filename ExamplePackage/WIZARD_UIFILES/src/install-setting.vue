<template>
  <pkg-center-step-content>
    <v-form syno-id="form" ref="form" :rules="rules">
      <v-form-item syno-id="form-item-input" prop="password" :label="newPasswordLabel" control-flex="230px">
        <v-input syno-id="input" v-model="password" />
      </v-form-item>
      <v-form-item syno-id="form-item-input" :label="confirmPasswordLabel" control-flex="230px">
        <v-input syno-id="input" v-model="confirmPassword" />
      </v-form-item>
      <v-form-item syno-id="form-item-input" :label="portLabel" control-flex="230px">
        <v-input syno-id="input" v-model="port" />
      </v-form-item>
    </v-form>
  </pkg-center-step-content>
</template>

<script>
import { $t } from './utils/uistring';
import { defineComponent, ref, watchEffect } from 'vue';

export default defineComponent({
  props: {
    ...SYNO.SDS.PkgManApp.Custom.useHook.props,
  },
  setup(props) {
    const form = ref(undefined)
    const { getNext, checkState: _checkState } = SYNO.SDS.PkgManApp.Custom.useHook(props);

    const checkState = async (owner) => {
      owner = owner ?? props.getOwner();
      _checkState(owner);
      const nextButton = owner.getButton('next');
      const isFormValid = await form.value?.validate();
      nextButton.setDisabled(!isFormValid);
    };

    watchEffect(() => {
      checkState();
    });

    const rules = {
      password: {
        validator: (rule, value, callback) => {
          // Your password rule
          if (value.length < 10) {
            return callback(new Error($t(_S('lang'), 'mariadb10', 'invalid_user_password_2')));
          }
          return callback();
        }
      },
    }

    const password = ref('')
    const confirmPassword = ref('')
    const port = ref('')
    const headline = $t(_S('lang'), 'wizard', 'wizard_set_data_title');

    const getValues = () => {
      return {
        pkgwizard_new_root_password: password.value,
        pkgwizard_port: port.value
      };
    };

    return {
      form,
      rules,
      password,
      confirmPassword,
      port,
      getNext,
      checkState,
      headline,
      getValues,
      newPasswordLabel: $t(_S('lang'), 'ui', 'db_new_password'),
      confirmPasswordLabel: $t(_S('lang'), 'ui', 'db_confirm_password'),
      portLabel: $t(_S('lang'), 'wizard', 'port'),
    };
  },
});
</script>
