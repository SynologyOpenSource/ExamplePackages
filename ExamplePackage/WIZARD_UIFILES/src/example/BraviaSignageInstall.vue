<template>
  <pkg-center-step-content>
    <v-form syno-id="form" :rules="rules" ref="form">
      <v-form-item syno-id="form-item-desc" hide-label textonly> {{ portInfoDesc }} </v-form-item>
      <v-form-item syno-id="form-item-port" prop="port" :label="portLabel" :indent="1" control-flex="210px">
        <v-input syno-id="port" v-model="port" number-only />
      </v-form-item>
      <v-form-item syno-id="form-item-desc2" hide-label textonly> {{ userInfoDesc }} </v-form-item>
      <v-form-item syno-id="form-item-username" prop="username" :label="usernameLabel" :indent="1" control-flex="210px">
        <v-input syno-id="username" v-model="username" />
      </v-form-item>
      <v-form-item syno-id="form-item-password" prop="password" :label="pwdLabel" :indent="1" control-flex="210px">
        <v-input type="password" syno-id="password" v-model="password" />
      </v-form-item>
      <v-form-item syno-id="form-item-confirmPassword" prop="confirmPassword" :label="confirmPwdLabel" :indent="1" control-flex="210px">
        <v-input type="password" syno-id="confirm-password" v-model="confirmPassword" />
      </v-form-item>
      <v-form-item syno-id="form-item-checkbox" hide-label textonly>
        <v-checkbox v-model="disableAuth" syno-id="checkbox">
          {{ disableAuthDesc }}
        </v-checkbox>
      </v-form-item>
    </v-form>
  </pkg-center-step-content>
</template>

<script>
import { defineComponent, ref, watchEffect } from 'vue';

export default defineComponent({
  props: {
    ...SYNO.SDS.PkgManApp.Custom.useHook.props,
  },
  setup(props) {
    const { getNext, checkState: _checkState } = SYNO.SDS.PkgManApp.Custom.useHook(props);
    const form = ref(undefined)
    const port = ref('');
    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const disableAuth = ref(false);

    const checkState = async(owner) => {
      owner = owner ?? props.getOwner();
      _checkState(owner);
      const nextButton = owner.getButton('next');
      let isFormValid = false;
      if (form.value?.isDirty()) {
        isFormValid = await form.value?.validate();
      }
      nextButton.setDisabled(!isFormValid);
    };

    watchEffect(() => {
      checkState();
    });

    const rules = {
      port: {
        required: true,
        validator: (rule, value, callback) => {
          if (value > 65535 || value < 1) {
            return callback(new Error('port invalid'));
          }
          return callback();
        }
      },
      username: {
        required: true,
      },
      password: {
        required: true,
        validator: (rule, value, callback) => {
          if (value.length < 12) {
            return callback(new Error("Password must >= 12 characters"));
          }
          return callback();
        }
      },
      confirmPassword: {
        required: true,
        validator: (rule, value, callback) => {
          if (!password.value) {
            return callback();
          }
          if (password.value !== value) {
            return callback(new Error('Confirm Password not match'));
          }
          return callback();
        }
      },
    }

    const headline = 'Configure BRAVIA Signage';

    const getValues = () => {
      return {
        pkgwizard_port: port.value,
        pkgwizard_username: username.value,
        pkgwizard_password: password.value,
        pkgwizard_disable_auth: disableAuth.value,
      };
    };
    
    return {
      form,
      rules,
      port,
      username,
      password,
      confirmPassword,
      disableAuth,
      getNext,
      checkState,
      headline,
      getValues,
      portInfoDesc: 'Please enter the port number of BRAVIA Signage.',
      portLabel: 'Port(1-65535):',
      userInfoDesc: 'Please enter the user name and password used for authentication.',
      usernameLabel: 'Username:',
      pwdLabel: 'Password:',
      confirmPwdLabel: 'Confirm Password:',
      disableAuthDesc: 'Disable Authentication'
    };
  },
});
</script>
