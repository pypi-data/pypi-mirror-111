import React from "react";

import { FeatherModel } from "@feather-ai/feather-web-components";
import "@feather-ai/feather-web-components/dist/main.css";

class App extends React.Component {
  render() {
    return (
      <>
        <FeatherModel isLocal={true} />
      </>
    );
  }
}
export default App;
