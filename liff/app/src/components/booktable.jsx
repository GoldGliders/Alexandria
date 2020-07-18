import React from "react"
import { initializeLiff } from "./liffInit"
import MultiButton from "./multibutton"
import liff from "@line/liff"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import CardMedia from "@material-ui/core/CardMedia"
import Grid from "@material-ui/core/Grid"
import Typography from "@material-ui/core/Typography"
import { withStyles } from "@material-ui/core/styles"

const useStyles = ((theme) => ({
  root: {
    flexGrow: 1,
  },
  card: {
    height: "auto",
    width: "100%",
    maxWidth: 400,
  },
  button: {
    align: "center"
  },
  media: {
    padding: 0,
    margin: 0,
  },
  image: {
    height: 150,
    width: "auto",
  },
  textarea: {
    textAlign: "center",
    width: "100%",
    padding: 0,
    "&:last-child": {
      paddingBottom: 0
    },
  },
  text: {
    marginTop: 4,
    padding: 0,
  }
}))

class BookTable extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      timestamps: [],
      bookmetas: [],
      uri: this.props.uri,
      columnNames: this.props.columnNames,
      liffId: this.props.liffId,
      os: null,
      error: null,
      erro_msg: null,
    }
    this.getResource = this.getResource.bind(this)
    this.row = this.row.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/${this.state.uri}?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const timestamps = res["items"].map(x => new Date(x["timestamp"]*1000).toLocaleDateString())
          const rows = res["items"].map(item => this.state.columnNames.map(key => item["bookmeta"][key]))

          this.setState({
            timestamps: timestamps.reverse(),
            bookmetas: rows.reverse(),
            os: resp["os"],
            error: false
          })
        })
        .catch((err) => {
          this.setState({
            timestamps: null,
            bookmetas: null,
            error: true,
            error_msg: err.message
          })
          liff.logout()
        })
    }else{
      this.setState({
        timestamps: null,
        bookmetas: null,
        error: true,
        error_msg: 503
      })
      liff.logout()
    }
  }

  multiButton(uri, isbn, title, os){
    switch(uri){
      case "history":
        if (os === "web"){
          return null
        }else{
          return <MultiButton funcName={uri} text="search" isbn={isbn}/>
        }

      case "bookmark":
        return  <MultiButton funcName={uri} text="remove" isbn={isbn} title={title} idToken={liff.getIDToken()}/>
    }
  }

  row(classes){
    const rows = this.state.bookmetas.map((bookmeta, rowNum) => {

      const metadata = (name) => bookmeta[this.state.columnNames.indexOf(name)]
      const title = metadata("title")
      const isbn = metadata("isbn")
      const author = metadata("author")

      return (
        <Grid container justify="center" alignItems="center" key={rowNum} item xs={12} zeroMinWidth>
          <Card variant="outlined" className={classes.card}>
            <CardActions className={classes.media}>
              <CardMedia
                component="img"
                image={`https://cover.openbd.jp/${isbn}.jpg`}
                title={title}
                className={classes.image}
              />
              <CardContent className={classes.textarea}>
                <Grid container>
                  <Grid item xs={12} >
                    <Typography color="textPrimary" variant="body1" component="h2" className={classes.text}>
                      {title}
                    </Typography>
                  </Grid>
                  <Grid item xs={12} >
                    <Typography color="textSecondary" variant="body2" component="h3" className={classes.text}>
                      {author}
                    </Typography>
                  </Grid>
                  {/*
                  <Grid item xs={4}>
                    <Typography color="textPrimary" variant="body2" component="h6">
                      {isbn}
                    </Typography>
                  </Grid>
                  <Grid item xs={6} >
                    <Typography color="textPrimary" variant="body2" component="h6" className={classes.text}>
                      {this.state.timestamps[rowNum]}
                    </Typography>
                  </Grid>
                  */}
                  <Grid item xs={9}></Grid>
                  <Grid item xs={3}>
                    {this.multiButton(this.state.uri, isbn, title, this.state.os)}
                  </Grid>
                </Grid>
              </CardContent>
            </CardActions>
          </Card>
        </Grid>
      )}
    )

    return rows
  }


  render(){
    const {classes} = this.props
    if (this.state.error){
      return(
        <div>
          <h1>api server error</h1>
        </div>
      )
    }else{
      return(
        <div className={classes.root}>
          <Grid container spacing={1}>
            {this.row(classes)}
          </Grid>
        </div>
      )
    }
  }
}

export default withStyles(useStyles, {withTheme: true})(BookTable)
