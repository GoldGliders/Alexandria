MyComponent extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      timestamps: [],
      bookmetas: [],
      bookkeys: ["title", "author", "isbn"],
      isLoaded: false,
      error: null,
      liffId: "1654371886-xorapzM6"
    }
  }

  componentDidMount(){
    this.initializeLiff()
  }

  initializeLiff() {
    liff
      .init({
        liffId: this.state.liffId
      })
      .then(() => {
        // start to use LIFF's api
        if (liff.getOS() === "web" && liff.isLoggedIn() === false){
          liff.login()
          this.initializeLiff(myLiffId)
        }else{
          if (liff.isLoggedIn() === true){
            this.get_history(liff.getIDToken())
          }
        }
      })
      .catch((err) => {
        document.getElementById("root").textContent = err.message
      })
  }


  get_history(id_token)uri{
    fetch(`/api/history?id_token=${id_token}`)
      .then(res => res.json())
      .then(
        (result) => {
          const timestamps = Array.from(result["items"].map(x => new Date(x["timestamp"]*1000).toLocaleDateString()))
          const bookmetas = result["items"].map(item => this.state.bookkeys.map(key => item["bookmeta"][key]))

          this.setState({
            timestamps: timestamps.reverse(),
            bookmetas: bookmetas.reverse(),
            isLoaded: true
          })
        })
      .catch(
        (error) => {
          this.setState({
            isLoaded: true,
            error: true
          })
          liff.logout()
          document.getElementById("root").textContent = error
        }
      )
  }

  render(){
    const ths = (
      <tr>
        <th>timestamp</th>
        {this.state.bookkeys.map((key, num) => <th key={num}>{key}</th>)}
      </tr>
    )

    const history_col = this.state.bookmetas.map((bookmeta, n) => {
      const timestamp = (
        <td key={n}>
          {this.state.timestamps[n]}
        </td>
      )

      const tds = bookmeta.map((meta, num) => (
        <td key={num}>
          {meta}
        </td>
      ))

      const button = (
        <button key={n} onClick={() => {
            if (liff.getOS() === "web"){
              alert("Webbrosers cannot use this function")
            }else if (liff.isInClient()){
              liff.sendMessages([
                {
                  type: "text",
                  text: bookmeta.filter((x, n) => this.state.bookkeys[n] === "isbn")[0]
                }
              ])
                .then(() => {
                  liff.closeWindow()
                })
                .catch((err) => {
                  document.getElementById("root").textContent = err
                })
            }
        }}>
          Re-search
        </button>
      )


      return (
          <tr key={n}>
            {timestamp}
            {tds}
            {button}
          </tr>
      )
    })

    return(
      <div>
        <table>
          <thead>
            {ths}
          </thead>
          <tbody>
            {history_col}
          </tbody>
        </table>
      </div>
    )
  }
}

ReactDOM.render(
  <MyComponent />,
  document.getElementById("root")
)
