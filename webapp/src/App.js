import "./App.css";
import { BrowserRouter, Route, Switch, useHistory } from "react-router-dom";
import axios from "axios";

import LoginForm from "./Components/forms/login";
import SignUp from "./Components/forms/signup";
import Dashboard from "./Components/Dash/Dashboard";

axios.defaults.baseURL = "http://127.0.0.1:5000";
//localStorage.setItem("token", null);

function Reroute() {
  const history = useHistory();

  !!localStorage.getItem("token")
    ? history.push("/login")
    : history.push("/dashboard");

  return <h1>Loading</h1>;
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route path="/login">
            <LoginForm />
          </Route>
          <Route path="/signup">
            <SignUp />
          </Route>
          <Route path="/dashboard">
            {!!localStorage.getItem("token") ? <Dashboard /> : <Reroute />}
          </Route>
          <Route path="/">
            <Reroute />
          </Route>
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
