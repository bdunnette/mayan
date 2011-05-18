import errno
import os

from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from document_indexing.models import IndexInstance

from metadata.classes import MetadataObject

from document_indexing.conf.settings import FILESERVING_ENABLE
from document_indexing.conf.settings import FILESERVING_PATH
from document_indexing.conf.settings import SLUGIFY_PATHS
#from document_indexing.conf.settings import MAX_RENAME_COUNT

if SLUGIFY_PATHS == False:
    #Do not slugify path or filenames and extensions
    SLUGIFY_FUNCTION = lambda x: x
else:
    SLUGIFY_FUNCTION = slugify


def get_instance_path(index_instance):
    """
    Return a platform formated filesytem path corresponding to an
    index instance
    """
    return os.sep.join(index_instance.get_ancestors().values_list(u'value', flat=True))


def fs_create_index_directory(index_instance):
    if FILESERVING_ENABLE:
        target_directory = os.path.join(FILESERVING_PATH, get_instance_path(index_instance))
        try:
            os.makedirs(target_directory)
            #next_available_filename(document, metadata_index, target_directory, SLUGIFY_FUNCTION(document.file_filename), SLUGIFY_FUNCTION(document.file_extension))
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                pass
            else:
                raise OSError(_(u'Unable to create metadata indexing directory: %s') % exc)    


def document_delete_fs_links(document):
    if FILESERVING_ENABLE:
        pass
        '''
        for document_metadata_index in document.documentmetadataindex_set.all():
            try:
                os.unlink(document_metadata_index.filename)
                document_metadata_index.delete()
            except OSError, exc:
                if exc.errno == errno.ENOENT:
                    #No longer exits, so delete db entry anyway
                    document_metadata_index.delete()
                else:
                    raise OSError(_(u'Unable to delete metadata indexing symbolic link: %s') % exc)

            path, filename = os.path.split(document_metadata_index.filename)

            #Cleanup directory of dead stuff
            #Delete siblings that are dead links
            try:
                for f in os.listdir(path):
                    filepath = os.path.join(path, f)
                    if os.path.islink(filepath):
                        #Get link's source
                        source = os.readlink(filepath)
                        if os.path.isabs(source):
                            if not os.path.exists(source):
                                #link's source is absolute and doesn't exit
                                os.unlink(filepath)
                        else:
                            os.unlink(os.path.join(path, filepath))
                    elif os.path.isdir(filepath):
                        #is a directory, try to delete it
                        try:
                            os.removedirs(path)
                        except:
                            pass
            except OSError, exc:
                pass

            #Remove the directory if it is empty
            try:
                os.removedirs(path)
            except:
                pass
        '''


def next_available_filename(document, metadata_index, path, filename, extension, suffix=0):
    target = filename
    if suffix:
        target = '_'.join([filename, unicode(suffix)])
    filepath = os.path.join(path, os.extsep.join([target, extension]))
    matches = DocumentMetadataIndex.objects.filter(filename=filepath)
    if matches.count() == 0:
        document_metadata_index = DocumentMetadataIndex(
            document=document, metadata_index=metadata_index,
            filename=filepath)
        try:
            os.symlink(document.file.path, filepath)
            document_metadata_index.save()
        except OSError, exc:
            if exc.errno == errno.EEXIST:
                #This link should not exist, try to delete it
                try:
                    os.unlink(filepath)
                    #Try again with same suffix
                    return next_available_filename(document, metadata_index, path, filename, extension, suffix)
                except Exception, exc:
                    raise Exception(_(u'Unable to create symbolic link, filename clash: %(filepath)s; %(exc)s') % {'filepath': filepath, 'exc': exc})
            else:
                raise OSError(_(u'Unable to create symbolic link: %(filepath)s; %(exc)s') % {'filepath': filepath, 'exc': exc})

        return filepath
    else:
        if suffix > MAX_RENAME_COUNT:
            raise Exception(_(u'Maximum rename count reached, not creating symbolic link'))
        return next_available_filename(document, metadata_index, path, filename, extension, suffix + 1)


#TODO: diferentiate between evaluation error and filesystem errors
def do_recreate_all_links(raise_exception=True):
    errors = []
    warnings = []

    for document in Document.objects.all():
        try:
            document_delete_fs_links(document)
        except NameError, e:
            warnings.append('%s: %s' % (document, e))
        except Exception, e:
            if raise_exception:
                raise Exception(e)
            else:
                errors.append('%s: %s' % (document, e))

    for document in Document.objects.all():
        try:
            create_warnings = document_create_fs_links(document)
        except Exception, e:
            if raise_exception:
                raise Exception(e)
            else:
                errors.append('%s: %s' % (document, e))

    for warning in create_warnings:
        warnings.append('%s: %s' % (document, warning))
    return errors, warnings