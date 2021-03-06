hqDefine("app_manager/js/settings/app_logos", function () {
    var self = {};
    var HQMediaUploaders = hqImport("hqmedia/js/hqmediauploaders").get(),
        initial_page_data = hqImport("hqwebapp/js/initial_page_data").get;
    var refs = initial_page_data('media_refs');
    var media_info = initial_page_data('media_info');

    var imageRefs = {};
    for (var slug in refs) {
        imageRefs[slug] = hqImport('hqmedia/js/hqmedia.reference_controller').ImageReference(refs[slug]);
        imageRefs[slug].upload_controller = HQMediaUploaders[slug];
        imageRefs[slug].setObjReference(media_info[slug]);
    }

    self.urlFromLogo = function (slug) {
        return imageRefs[slug].url;
    };

    self.thumbUrlFromLogo = function (slug) {
        return imageRefs[slug].thumb_url;
    };

    self.triggerUploadForLogo = function (slug) {
        if (imageRefs[slug]) {
            imageRefs[slug].triggerUpload();
        }
    };

    self.uploadCompleteForLogo = function (slug, response) {
        if (imageRefs[slug]) {
            imageRefs[slug].uploadComplete(null, null, response);
        }
    };

    self.getPathFromSlug = function (slug) {
        return imageRefs[slug].path;
    };

    self.removeLogo = function (slug) {
        $.post(
            hqImport("hqwebapp/js/initial_page_data").reverse("hqmedia_remove_logo"),
            {
                logo_slug: slug,
            },
            function (data, status) {
                if (status === 'success') {
                    imageRefs[slug].url("");
                }
            }
        );
    };

    return {
        LogoManager: self,
    };
});
