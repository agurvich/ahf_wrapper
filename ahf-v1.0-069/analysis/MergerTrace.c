/*==================================================================================================
 *
 *  MergerTrace:   use AHF_halos and MergerTree's _mtree_idx file to follow individual haloes
 *
 *  WARNING:
 *     this code is not tuned for performance and works better the fewer haloes are traced!
 *            
 *==================================================================================================*/

#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <inttypes.h>
#include <assert.h>
#include <libgen.h>
#include <ctype.h>

#include "../src/param.h"
#include "../src/tdef.h"
#include "../src/common.c"
#include "../src/libutility/utility.h"

/*-------------------------------------------------------------------------------------
 *                                  THE STRUCTURES
 *-------------------------------------------------------------------------------------*/


/*-------------------------------------------------------------------------------------
 *                                 GLOBAL VARIABLES
 *-------------------------------------------------------------------------------------*/
char **AHF_halos;
char **mtree_idx;
int  num_files;

uint64_t *haloid;
int  num_haloid;


/*-------------------------------------------------------------------------------------
 *                                    PROTOTYPES
 *-------------------------------------------------------------------------------------*/
void     get_filename_list(char *);
void     get_haloid_list(char *);
void     get_headerline(char *, char*);
void     get_haloline(char *, uint64_t, char*);
int64_t  get_haloidx(char *, uint64_t);
double   get_redshift(char *);


/*==================================================================================================
 * main:
 *
 *       simply a wrapper for successive calls to create_mtree()
 *
 *==================================================================================================*/
int main(argc,argv)
int argc;
char **argv;
{
  FILE *fpout;
  char prefix_list[MAXSTRING], haloid_list[MAXSTRING], outfile[MAXSTRING], haloline[MAXSTRING];
  int i, n;
  int64_t ihalo;
  double z;
  
  /*==================================================================*
   *                          USER INTERFACE                          *
   *==================================================================*/
  if(argc<3)
   {
    fprintf(stderr,"usage: %s haloid_list prefix_list\n",*argv);
    exit(1);
   }
  strcpy(haloid_list,    argv[1]);
  strcpy(prefix_list,    argv[2]);

  fprintf(stderr,"=======================================================================\n");
  fprintf(stderr,"               follow AHF_halos through _mtree_idx files\n");
  fprintf(stderr,"=======================================================================\n");
  fprintf(stderr,"will read mtree_idx and AHF_halos files using prefixes found in %s\n",prefix_list);
  fprintf(stderr,"will read haloids to follow from %s\n\n",haloid_list);
  
  /*==================================================================*
   *                          READ USER DATA                          *
   *==================================================================*/
  get_haloid_list(haloid_list);
  get_filename_list(prefix_list);
  
  
  /*==================================================================*
   *                            DO THE WORK                           *
   *==================================================================*/
  for(i=0; i<num_haloid; i++) {
    ihalo = haloid[i];
    fprintf(stderr," + tracing halo %"PRIu64" through %d files: ",ihalo,num_files);
    
    // open outfile for this halo
    sprintf(outfile,"halo_%05"PRIu64".dat",ihalo);
    fpout = fopen(outfile,"w");
    assert(fpout != NULL);
    
    // copy header line from AHF_halos[0] (assuming they all have the same header)
    get_headerline(AHF_halos[0], haloline);
    // Get rid of the comment format in front of the ID
    memmove(haloline, haloline+1, strlen(haloline));
    fprintf(fpout,"#redshift(0)\t %s",haloline);
    
    // loop over all files
    for(n=0; n<num_files-1; n++) {
      get_haloline(AHF_halos[n], ihalo, haloline);
      z = get_redshift(AHF_halos[n]);
      fprintf(fpout,"%f\t%s",z,haloline);
      ihalo = get_haloidx(mtree_idx[n], ihalo);
      fprintf(stderr,"%"PRIi64" ",ihalo);
      if(ihalo < 0)
        break;
    }
    fprintf(stderr,"\n");
    get_haloline(AHF_halos[n], ihalo, haloline);
    z = get_redshift(AHF_halos[n]);
    fprintf(fpout,"%f\t%s",z,haloline);
    
    // close output file
    fclose(fpout);
  }
  
  
  
  /*==================================================================*
   *                              BYE-BYE                             *
   *==================================================================*/
  free(haloid);
  for(i=0; i<num_files; i++) {
    free(AHF_halos[i]);
    free(mtree_idx[i]);
  }
  free(AHF_halos);
  free(mtree_idx);
  
  printf("DONE\n");
  return(0);
}

/*==================================================================================================
 * get_filenam_list
 *==================================================================================================*/
void get_filename_list(char *prefix_list)
{
  FILE *fp;
  char line[MAXSTRING];
  int  i;
  
  // open file
  fp = fopen(prefix_list,"r");
  assert(fp != NULL);

  // figure out number of AHF_halos files
  num_files = 0;
  while(!feof(fp)) {
    fgets(line,MAXSTRING,fp);
    num_files++;
  }
  num_files--; // we counted one too many
  
  // allocate memory
  AHF_halos = (char **) calloc(num_files, sizeof(char *));
  mtree_idx = (char **) calloc(num_files, sizeof(char *));
  
  // eventually read haloids
  fprintf(stderr," + will use the following files for the tracing:\n");
  rewind(fp);
  for(i=0; i<num_files; i++) {
    fscanf(fp,"%s",line);
    AHF_halos[i] = (char *) calloc(MAXSTRING,sizeof(char));
    mtree_idx[i] = (char *) calloc(MAXSTRING,sizeof(char));
    sprintf(AHF_halos[i],"%s_halos",line);
    sprintf(mtree_idx[i],"%s_mtree_idx",line);
    if(i==num_files-1)
      fprintf(stderr,"     %s\n", AHF_halos[i]);
    else
      fprintf(stderr,"     %s, %s\n", AHF_halos[i], mtree_idx[i]);      
  }
  
  // close file
  fclose(fp);
}

/*==================================================================================================
 * get_haloid_list
 *==================================================================================================*/
void get_haloid_list(char *haloid_list)
{
  FILE *fp;
  char line[MAXSTRING];
  int  i;
  
  // open file
  fp = fopen(haloid_list,"r");
  assert(fp != NULL);
  
  // figure out number of haloids
  num_haloid = 0;
  while(!feof(fp)) {
    fgets(line,MAXSTRING,fp);
    num_haloid++;
  }
  num_haloid--; // we counted one too many
  
  // allocate memory
  haloid = (uint64_t *) calloc(num_haloid, sizeof(uint64_t));
  
  // eventually read haloids
  fprintf(stderr," + found %d haloids to be traced:\n",num_haloid);
  rewind(fp);
  for(i=0; i<num_haloid; i++) {
    fgets(line,MAXSTRING,fp);
    sscanf(line,"%"SCNu64,&(haloid[i]));
    if(i == num_haloid-1)
      fprintf(stderr,"     %"PRIu64,haloid[i]);
    else
      fprintf(stderr,"     %"PRIu64", ",haloid[i]);      
  }
  fprintf(stderr,"\n");

  // close file
  fclose(fp);  
}


/*==================================================================================================
 * get_headerline
 *==================================================================================================*/
void get_headerline(char *halofile, char *line)
{
  FILE *fp;
  int64_t haloid;
  
  fp = fopen(halofile,"r");
  assert(fp != NULL);
  
  strcpy(line,"a");
  while(strncmp(line,"#",1) != 0 && !feof(fp)) {
    fgets(line,MAXSTRING,fp);
  }
  
  if(feof(fp)) {
    fclose(fp);
    strcpy(line,"# could not find any header!?\n");
  }
  else {
    fclose(fp);
  }
}

/*==================================================================================================
 * get_haloline
 *==================================================================================================*/
void get_haloline(char *halofile, uint64_t id, char *line)
{
  FILE *fp;
  int64_t haloid;

  fp = fopen(halofile,"r");
  assert(fp != NULL);
  
  haloid = -1;
  while(haloid != id && !feof(fp)) {
    fgets(line,MAXSTRING,fp);
    if(strncmp(line,"#",1) != 0)
      sscanf(line,"%"SCNi64,&haloid);
    else
      haloid = -1;
  }
  
  if(feof(fp)) {
    fclose(fp);
    strcpy(line,"-1\n");
  }
  else {
    fclose(fp);
  }
}

/*==================================================================================================
 * get_haloidx
 *==================================================================================================*/
int64_t get_haloidx(char *halofile, uint64_t id)
{
  FILE *fp;
  int64_t haloid, haloidx;
  char line[MAXSTRING];
  
  fp = fopen(halofile,"r");
  assert(fp != NULL);
    
  haloid = -1;
  while(haloid != id && !feof(fp)) {
    fgets(line,MAXSTRING,fp);
    if(strncmp(line,"#",1) != 0)
      sscanf(line,"%"SCNi64,&haloid);
    else
      haloid = -1;
  }

  if(feof(fp)) {
    fclose(fp);
    return(-1);
  }
  else {
    sscanf(line,"%"SCNu64"%"SCNu64,&haloid,&haloidx);
    return(haloidx);
  }
  
}

/*==================================================================================================
 * get_redshift
 *==================================================================================================*/
double get_redshift(char *prefix)
{
	double z    = -99.0;
	int    zIdx = strlen(prefix);
    
  // ignore all EOS's
  while(prefix[zIdx] == '\0')
    zIdx--;
  
  // hunt down the 'z'
  while(prefix[zIdx] != 'z')
    zIdx--;
  
	if (prefix[zIdx] == 'z') {
		(void)sscanf(prefix + zIdx, "z%lf", &z);
	}
  
	return z;
}


