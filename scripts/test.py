from pylovepdf.ilovepdf import ILovePdf


def compress_shit(name, pdfname):
    ilovepdf = ILovePdf(
        'project_public_276c710d7c4588dcd67beeb2c6ca32cf_ryCHU12c034b3785a296ed06c35cd02588ee8', verify_ssl=True)
    task = ilovepdf.new_task('compress')
    task.add_file(pdfname)
    task.output_filename = name+'_compressed'
    task.downloaded_filename = name+'_compressed.pdf'
    task.set_output_folder('./Output')
    task.execute()
    task.download()
    task.delete_current_task()


if __name__ == '__main__':
    print("hello")


# custom text dynamic text with different size try
# st.markdown("""
#     <style>
#     .big-font {
#         font-size: 40px !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<p class="big-font">"%s" % s</p>',
#             unsafe_allow_html=True)
