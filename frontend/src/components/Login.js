import React, { Component } from "react";
// import $ from "jquery";
import "../stylesheets/Login.css";

class Login extends Component {
  constructor() {
    super();
    this.state = {
      tokenCilent:
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0MDFhYzdjNDAzZGRlNmEyNWFlMTkiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5NjA1MjUsImV4cCI6MTY5ODk2NzcyNSwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzLWNhdGVnb3J5X2lkLXF1ZXN0aW9ucyIsInBhdGNoOnF1aXp6ZXMiLCJwb3N0OnF1ZXN0aW9ucyJdfQ.hnPCsLdyvTL4qHIOjDP9RuiVnjpkCWyK_oDIODDjzRHH0N8MrY4EzarLdkUAZcGU1J_f3YinS95jAFLdTaaJ6xI0TVbFQI2e_YAdgMXkyr4DgDCI1Wxy4VOuN1Vqfvsi3PoV6tM8sfWT9_CD9CRDBp5IbIxitAti0YxMw6Iv9dLI--RgI9MkNeH0kiYEjRgqS8CvQkLuAU4MMxhYb0PB2nSbb8Z_8It3Lo4v8FgtekMzgYgDTei7Eif3QCcy7PN2FevZwAN-eILyI8b3ZTKGiOBA-AIvSnjPKh0ASIbOoJMOkOgwvjK7aTfErXaTedZ3l5eBDsGE1XE3q4Qc8B75jA",
      tokenEmployee:
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0MDIzMWNiYTJmZWEyNjE4ZTMzZDIiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5NjA4MDUsImV4cCI6MTY5ODk2ODAwNSwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpxdWVzdGlvbnMiLCJnZXQ6Y2F0ZWdvcmllcy1jYXRlZ29yeV9pZC1xdWVzdGlvbnMiLCJwYXRjaDpxdWl6emVzIiwicG9zdDpxdWVzdGlvbnMiXX0.SI2xRJw2Q7TsxshdxD9GImt_jaYKtQ66KCqPBTHYpX18qwWAnl1UYZAHcs38uT6N7VTCLVYqEXr2aQoNoEcCNq8uE1SLzurMSg592XWXz2E6lp5vjdnffTOOp-oG9J9UPAL9HwQsojLaXdX3ruYsgQQLZPBvofEduVXnmqrud0mTz_mjWS6zkHXBTo5uE-Gj1sE_pvoXv8AfEuH4bzkQZXddk6UkdH7fDmlzefFX2brHvW9EiOntjyCBqZw5WmmRQinie_5ewJ-QhisbV0S3LCo3WdoVQVChwGKOqwDHIBh88Fu_as1nBfk8ZlNo4A9ygizi_LOIoG-_1ypK0gQP0w",
    };
  }
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  login = (type) => {
    if (type === 1) localStorage.setItem("token", this.state.tokenCilent);
    else localStorage.setItem("token", this.state.tokenCilent);
    this.navTo("/home");
  };

  render() {
    return (
      <div className="button-container">
        <button
          onClick={() => {
            this.navTo("/home");
          }}
        >
          Guest User
        </button>
        <button
          onClick={() => {
            this.login(1);
          }}
        >
          Login Client User
        </button>
        <button
          onClick={() => {
            this.login(2);
          }}
        >
          Login Cilent Employee
        </button>
      </div>
    );
  }
}

export default Login;
