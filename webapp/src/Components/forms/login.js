import React, { useCallback } from "react";
import {
  Avatar,
  Button,
  CssBaseline,
  Grid,
  Link,
  Paper,
  TextField,
  Typography,
} from "@material-ui/core";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import { makeStyles } from "@material-ui/core/styles";
import { useFormik } from "formik";
import axios from "axios";
import * as Yup from "yup";
import { useHistory } from "react-router-dom";

const loginDefault = {
  username: "",
  password: "",
};

const LoginScheme = () =>
  Yup.object().shape({
    username: Yup.string().required("Username can't be empty"),
    password: Yup.string().required("password can't be empty"),
  });

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100vh",
  },
  image: {
    backgroundImage: "url(https://source.unsplash.com/random)",
    backgroundRepeat: "no-repeat",
    backgroundColor:
      theme.palette.type === "light"
        ? theme.palette.grey[50]
        : theme.palette.grey[900],
    backgroundSize: "cover",
    backgroundPosition: "center",
  },
  paper: {
    margin: theme.spacing(8, 4),
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
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function LoginForm() {
  const classes = useStyles();
  const history = useHistory();

  const redirectToHome = useCallback(() => {
    console.log("logged in");
    history.push("/dashboard");
  }, []);

  const saveJWT = (token, username) => {
    if (!!token) {
      localStorage.setItem("token", token);
      localStorage.setItem("username", username);
    }

    redirectToHome();
  };

  const onSubmit = async (values) => {
    try {
      console.log(values);
      const { status, data, statusText } = await axios.post("/login/", {
        data: {
          ...values,
        },
      });
      switch (status) {
        case 200:
          saveJWT(data[0]["Auth"], values.username);
          break;
        case 401:
        case 404:
        default:
          throw new Error(statusText);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const formik = useFormik({
    validationSchema: LoginScheme,
    initialValues: loginDefault,
    onSubmit,
  });

  return (
    <Grid container component="main" className={classes.root}>
      <CssBaseline />
      <Grid item xs={false} sm={4} md={7} className={classes.image} />
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign In
          </Typography>
          <form className={classes.form} onSubmit={formik.handleSubmit}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="Username"
              autoComplete="Username"
              autoFocus
              onChange={(e) => {
                formik.setFieldTouched("username");
                formik.setFieldValue("username", e.target.value);
              }}
              error={!formik.touched.username}
            />
            <TextField
              variant="outlined"
              margin="normal"
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
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              disabled={Boolean(
                !formik.isValid ||
                  !formik.touched.username ||
                  !formik.touched.password
              )}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item>
                <Link href="/signup" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
      </Grid>
    </Grid>
  );
}
