import React, { useCallback } from "react";
import {
  Avatar,
  Button,
  Container,
  CssBaseline,
  Grid,
  Link,
  TextField,
  Typography,
} from "@material-ui/core";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import { makeStyles } from "@material-ui/core/styles";
import { useFormik } from "formik";
import axios from "axios";
import * as Yup from "yup";
import { useHistory } from "react-router-dom";
import { useSetRecoilState } from "recoil";

import { tokenState } from "../atoms";

const signUpDefault = {
  username: "",
  password: "",
  firstname: "",
  lastname: "",
};

const SignUpScheme = () =>
  Yup.object().shape({
    username: Yup.string().required("Username can't be empty"),
    password: Yup.string().required("password can't be empty"),
    firstname: Yup.string().required("first name can't be empty"),
    lastname: Yup.string().required("last name can't be empty"),
  });

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%",
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function SignUp() {
  const classes = useStyles();

  const history = useHistory();
  const setToken = useSetRecoilState(tokenState);

  const redirectToHome = useCallback(() => {
    console.log("Signed up");
    console.log("logged in");
    history.push("/dashboard");
  }, []);

  const saveJWT = (token) => {
    console.log({ token });
    if (!!token) {
      localStorage.setItem("token", token);
      axios.defaults.headers["Auth"] = token;
    }
    setToken(token);
    redirectToHome();
  };

  const onSubmit = async (values) => {
    try {
      console.log(values);

      const { status, data, statusText } = await axios.post("/signup/", {
        data: {
          ...values,
        },
      });

      if (status === 200) {
        saveJWT(data[0]["Auth"]);
      }

      if (status === 401) {
        throw new Error(statusText);
      }

      if (status === 500) {
        throw new Error(statusText);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const formik = useFormik({
    validationSchema: SignUpScheme,
    initialValues: signUpDefault,
    onSubmit,
  });

  console.log(formik);

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <form className={classes.form} onSubmit={formik.handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                autoComplete="fname"
                name="firstName"
                variant="outlined"
                required
                fullWidth
                id="firstName"
                label="First Name"
                autoFocus
                onChange={(e) => {
                  formik.setFieldTouched("firstname");
                  formik.setFieldValue("firstname", e.target.value);
                }}
                error={!formik.touched.firstname}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="lastName"
                label="Last Name"
                name="lastName"
                autoComplete="lname"
                onChange={(e) => {
                  formik.setFieldTouched("lastname");
                  formik.setFieldValue("lastname", e.target.value);
                }}
                error={!formik.touched.lastname}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="username"
                label="User name"
                name="username"
                autoComplete="username"
                onChange={(e) => {
                  formik.setFieldTouched("username");
                  formik.setFieldValue("username", e.target.value);
                }}
                error={!formik.touched.username}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                onChange={(e) => {
                  formik.setFieldTouched("password");
                  formik.setFieldValue("password", e.target.value);
                }}
                error={!formik.touched.password}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            disabled={Boolean(
              !formik.isValid ||
                !formik.touched.username ||
                !formik.touched.password ||
                !formik.touched.firstname ||
                !formik.touched.lastname
            )}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item>
              <Link href="/login" variant="body2">
                Already have an account? Sign in
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
    </Container>
  );
}
