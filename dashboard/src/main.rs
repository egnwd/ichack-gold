#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate rocket;

use rocket::response::NamedFile;
use std::path::PathBuf;

#[get("/")]
fn index() -> Option<NamedFile> {
    NamedFile::open("static/index.html").ok()
}

#[get("/static/<path..>")]
fn static_files(path: PathBuf) -> Option<NamedFile> {
    let mut static_dir = PathBuf::from("static/");
    static_dir.push(path);
    NamedFile::open(static_dir).ok()
}

fn main() {
    rocket::ignite()
        .mount("/", routes![index, static_files])
        .launch();
}
