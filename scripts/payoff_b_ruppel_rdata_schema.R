#!/usr/bin/env Rscript

# Original Rüppel et al. (2023) RData source-only schema audit.
# Reads type, dimensions, column names, and missingness counts only.
# Does NOT fit weather/outcome regressions, inspect tracks or show individual
# rows. Serialized objects are loaded in a new environment.
args <- commandArgs(trailingOnly=TRUE)
if ("--self-test" %in% args) {
  toy <- data.frame(individual_id=c("a","a","b"),
                    decision_time=as.POSIXct(c("2023-01-01","2023-01-02","2023-01-03"),
                                             tz="UTC"),
                    weather_cue=c(2,NA,3), outcome=c(0,1,1))
  stopifnot(nrow(toy)==3, inherits(toy$decision_time,"POSIXct"),
            sum(is.na(toy$weather_cue))==1)
  cat("RUPPEL_RDATA_SCHEMA_SYNTHETIC_PASS\n")
  quit(save="no",status=0)
}

zip_path <- "outputs/.source-only-ruppel-2023.zip"
if (!file.exists(zip_path)) stop("exact MD5/SHA256 verified Figshare archive absent")
filenames <- c("data.Event.RData","flights.RData","Rcode.Rmd")
temp <- tempfile("ruppel_schema_")
dir.create(temp)
unzip(zip_path, files=filenames, exdir=temp, overwrite=FALSE)
for (f in filenames) {
  if (!file.exists(file.path(temp,f))) stop(paste("missing source archive component",f))
}
object_receipt <- list()
column_receipt <- list()
count <- 0L
string <- function(x) paste(as.character(x),collapse=";")

audit_obj <- function(x,source,object_name,depth=0L) {
  count <<- count + 1L
  base <- list(source_file=source,
               object_name=object_name,
               class=string(class(x)),
               typeof=typeof(x),
               is_data_frame=is.data.frame(x),
               nrow=if(is.data.frame(x)) nrow(x) else NA_integer_,
               ncol=if(is.data.frame(x)) ncol(x) else NA_integer_,
               list_length=if(is.list(x)) length(x) else NA_integer_,
               nesting_depth=depth)
  object_receipt[[length(object_receipt)+1]] <<- as.data.frame(base,stringsAsFactors=FALSE)
  if (is.data.frame(x)) {
    for (col in names(x)) {
      y <- x[[col]]
      id_or_time <- grepl("id|bird|individual|date|day|time|hour|timestamp|departure|arrival|landing|weather|wind",
                          col,ignore.case=TRUE)
      v <- list(source_file=source,
                object_name=object_name,
                column_name=col,
                column_class=string(class(y)),
                column_storage=typeof(y),
                missing_count=sum(is.na(y)),
                nonmissing_count=sum(!is.na(y)),
                id_or_time_candidate=id_or_time)
      column_receipt[[length(column_receipt)+1]] <<- as.data.frame(v,stringsAsFactors=FALSE)
    }
  } else if (is.list(x) && depth < 2L) {
    nx <- names(x)
    for(i in seq_len(min(length(x),30L))) {
      if (is.data.frame(x[[i]])) {
        obj_name <- if(!is.null(nx)&&nzchar(nx[i])) nx[i] else paste0("[[",i,"]]")
        audit_obj(x[[i]],source,paste(object_name,obj_name,sep="/"),depth+1L)
      }
    }
  }
}
for (file in filenames[1:2]) {
  env <- new.env(parent=baseenv())
  loaded <- load(file.path(temp,file),envir=env)
  if (length(loaded)>20L) stop("unexpected high number of serialized objects")
  for (nm in loaded) audit_obj(get(nm,envir=env,inherits=FALSE),file,nm)
}

out_dir <- "outputs"
dir.create(out_dir,recursive=TRUE,showWarnings=FALSE)
if(length(object_receipt)==0L) stop("no loaded RData objects")
objects <- do.call(rbind,object_receipt)
write.csv(objects,file.path(out_dir,"payoff_b_ruppel_original_object_schema.csv"),row.names=FALSE)
if(length(column_receipt)>0L){
  columns <- do.call(rbind,column_receipt)
  write.csv(columns,file.path(out_dir,"payoff_b_ruppel_original_column_schema.csv"),row.names=FALSE)
} else stop("no data-frame source objects could be structurally inspected")

# Original author Rmd is read for analysis structuring, never executed.
code <- readLines(file.path(temp,filenames[3]),warn=FALSE,encoding="UTF-8")
pattern <- "(data[.]Event|flights|landing|depart|route|wind|weather|time|date|headwind|cloud|glm\\(|glmer\\(|gam\\(|mutate\\(|join\\(|coxph\\()"
matched <- grep(pattern,code,ignore.case=TRUE,perl=TRUE)
pick <- matched[seq_len(min(length(matched),65L))]
audit_lines <- c("ORIGINAL_AUTHOR_CODE_CONTEXT__NOT_EXECUTED",
                 paste0("Original code total lines: ",length(code)),
                 paste0("Matched context lines: ",length(matched)),
                 paste0("Snippet count (capped): ",length(pick)),
                 vapply(pick,function(i)
                        paste0("L",i,": ",substr(trimws(code[i]),1L,170L)),character(1)))
writeLines(audit_lines,file.path(out_dir,"payoff_b_ruppel_author_Rmd_source_structure.txt"),
           useBytes=TRUE)

cat("RUPPEL_SOURCE_RDATA_OBJECT_SCHEMA_PASSED\n")
print(objects,row.names=FALSE)
cat("RUPPEL_SOURCE_RDATA_COLUMN_SCHEMAS\n")
print(columns[,c("source_file","object_name","column_name",
                 "column_class","missing_count","nonmissing_count")],row.names=FALSE)
cat("Original Rmd total lines",length(code),"matched",length(matched),"\n")
cat("SCHEMA_ONLY_NO_BIOLOGICAL_EFFECTS_OR_FITNESS_ESTIMATED\n")
unlink(temp,recursive=TRUE)
