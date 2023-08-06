# from __future__ import print_function, absolute_import, division
import logging
import math
import multiprocessing
import re
import shutil
import sys
import types
from pathlib import Path

import allesfitter
import numpy as np
import yaml
from argparse import ArgumentParser
from lcbuilder.star.HabitabilityCalculator import HabitabilityCalculator
import pandas as pd
import os
from os import path
import matplotlib.pyplot as plt


resources_dir = path.join(path.dirname(__file__))


class Fitter:
    def __init__(self, object_dir, only_initial, mcmc=False, detrend=None):
        self.args = types.SimpleNamespace()
        self.args.noshow = True
        self.args.north = False
        self.args.o = True
        self.args.auto = True
        self.args.save = True
        self.args.nickname = ""  # TODO do we set the sherlock id?
        self.args.FFI = False  # TODO get this from input
        self.args.targetlist = "best_signal_latte_input.csv"
        self.args.new_path = ""  # TODO check what to do with this
        self.object_dir = os.getcwd() if object_dir is None else object_dir
        self.latte_dir = str(Path.home()) + "/.sherlockpipe/latte/"
        if not os.path.exists(self.latte_dir):
            os.mkdir(self.latte_dir)
        self.data_dir = self.object_dir
        self.only_initial = only_initial
        self.mcmc = mcmc
        self.detrend = detrend

    def fit(self, candidate_df, star_df, cpus, allesfit_dir):
        candidate_row = candidate_df.iloc[0]
        logging.info("Preparing fit files")
        sherlock_star_file = self.object_dir + "/params_star.csv"
        star_file = allesfit_dir + "/params_star.csv"
        params_file = allesfit_dir + "/params.csv"
        settings_file = allesfit_dir + "/settings.csv"
        if candidate_row["number"] is None or np.isnan(candidate_row["number"]):
            lc_file = "/" + candidate_row["lc"]
        else:
            lc_file = "/" + str(candidate_row["number"]) + "/lc_" + str(candidate_row["curve"]) + ".csv"
        shutil.copyfile(self.object_dir + lc_file, allesfit_dir + "/lc.csv")
        if os.path.exists(sherlock_star_file) and os.path.isfile(sherlock_star_file):
            shutil.copyfile(sherlock_star_file, star_file)
        shutil.copyfile(resources_dir + "/resources/allesfitter/params.csv", params_file)
        shutil.copyfile(resources_dir + "/resources/allesfitter/settings.csv", settings_file)
        fit_width = 0.3333333
        if candidate_row["duration"] is not None:
            fit_width = float(candidate_row["duration"]) / 60 / 24 * 7
        # TODO replace sherlock properties from allesfitter files
        # TODO only use params_star when the star mass or radius was not assumed
        logging.info("Preparing fit properties")
        with open(settings_file, 'r+') as f:
            text = f.read()
            text = re.sub('\\${sherlock:cores}', str(cpus), text)
            text = re.sub('\\${sherlock:fit_width}', str(fit_width), text)
            text = re.sub('\\${sherlock:name}', str(candidate_row["name"]), text)
            if self.detrend == 'hybrid_spline':
                detrend_param = "baseline_flux_lc,hybrid_spline"
            elif self.detrend == 'gp':
                detrend_param = 'baseline_flux_lc,sample_GP_Matern32'
            else:
                detrend_param = ''
            text = re.sub('\\${sherlock:detrend}', detrend_param, text)
            f.seek(0)
            f.write(text)
            f.truncate()
        with open(params_file, 'r+') as f:
            text = f.read()
            text = re.sub('\\${sherlock:t0}', str(candidate_row["t0"]), text)
            text = re.sub('\\${sherlock:t0_min}', str(candidate_row["t0"] - 0.02), text)
            text = re.sub('\\${sherlock:t0_max}', str(candidate_row["t0"] + 0.02), text)
            text = re.sub('\\${sherlock:period}', str(candidate_row["period"]), text)
            text = re.sub('\\${sherlock:period_min}', str(candidate_row["period"] - candidate_row["per_err"]), text)
            text = re.sub('\\${sherlock:period_max}', str(candidate_row["period"] + candidate_row["per_err"]), text)
            if self.detrend == 'gp':
                baseline_params = 'baseline_gp_matern32_lnsigma_flux_lc,0.0,1,uniform -15.0 15.0,$\mathrm{gp: \ln{\sigma} (lc)}$,\n' + \
                    'baseline_gp_matern32_lnrho_flux_lc,0.0,1,uniform -15.0 15.0,$\mathrm{gp: \ln{\rho} (lc)}$,'
            else:
                baseline_params = ""
            text = re.sub('\\${sherlock:baseline_params}', baseline_params, text)
            rp_rs = candidate_row["rp_rs"] if candidate_row["rp_rs"] != "-" else 0.1
            depth = candidate_row["depth"] / 1000
            # TODO calculate depth error in SHERLOCK maybe given the std deviation from the depths or even using the residuals
            depth_err = depth * 0.2
            rp_rs_err = 0.5 / math.sqrt(depth) * depth_err
            text = re.sub('\\${sherlock:rp_rs}', str(rp_rs), text)
            rp_rs_min = rp_rs - 2 * rp_rs_err
            rp_rs_min = rp_rs_min if rp_rs_min > 0 else 0.0000001
            rp_rs_max = rp_rs + 2 * rp_rs_err
            rp_rs_max = rp_rs_max if rp_rs_max < 1 else 0.9999
            text = re.sub('\\${sherlock:rp_rs_min}', str(rp_rs_min), text)
            text = re.sub('\\${sherlock:rp_rs_max}', str(rp_rs_max), text)
            G = 6.674e-11
            mstar_kg = star_df.iloc[0]["M_star"] * 2e30
            mstar_kg_lerr = star_df.iloc[0]["M_star_lerr"] * 2e30
            mstar_kg_uerr = star_df.iloc[0]["M_star_uerr"] * 2e30
            rstar_au = star_df.iloc[0]['R_star'] * 0.00465047
            rstar_lerr_au = star_df.iloc[0]["R_star_lerr"] * 0.00465047
            rstar_uerr_au = star_df.iloc[0]["R_star_uerr"] * 0.00465047
            per = candidate_row["period"] * 24 * 3600
            per_err = candidate_row["per_err"] * 24 * 3600
            a = (G * mstar_kg * per ** 2 / 4. / (np.pi ** 2)) ** (1. / 3.)
            a_au = a / 1.496e11
            sum_rp_rs_a = (np.sqrt(depth) + 1.) * rstar_au / a_au
            sum_rp_rs_a_lerr = np.sqrt(
                np.square(0.5 * depth_err / depth) + np.square(rstar_lerr_au / rstar_au) + np.square(
                    2 * per_err / 3. / per) + np.square(mstar_kg_lerr / 3. / mstar_kg)) * sum_rp_rs_a
            sum_rp_rs_a_uerr = np.sqrt(
                np.square(0.5 * depth_err / depth) + np.square(rstar_uerr_au / rstar_au) + np.square(
                    2 * per_err / 3. / per) + np.square(mstar_kg_uerr / 3. / mstar_kg)) * sum_rp_rs_a
            sum_rp_rs_a_min = sum_rp_rs_a - 2 * sum_rp_rs_a_lerr
            sum_rp_rs_a_max = sum_rp_rs_a + 2 * sum_rp_rs_a_uerr
            sum_rp_rs_a_min = sum_rp_rs_a_min if sum_rp_rs_a_min > 0 else 0.0000001
            text = re.sub('\\${sherlock:sum_rp_rs_a}', str(sum_rp_rs_a), text)
            text = re.sub('\\${sherlock:sum_rp_rs_a_min}', str(sum_rp_rs_a_min), text)
            text = re.sub('\\${sherlock:sum_rp_rs_a_max}', str(sum_rp_rs_a_max), text)
            text = re.sub('\\${sherlock:name}', str(candidate_row["name"]), text)
            # TODO this check is wrong and might need to check whether ld_a and ld_b exist within the dataframe
            if os.path.exists(sherlock_star_file) and os.path.isfile(sherlock_star_file):
                text = re.sub('\\${sherlock:ld_a}', str(star_df.iloc[0]["ld_a"]), text)
                text = re.sub('\\${sherlock:ld_b}', str(star_df.iloc[0]["ld_b"]), text)
            else:
                text = re.sub('\\${sherlock:ld_a}', "0.5", text)
                text = re.sub('\\${sherlock:ld_b}', "0.5", text)
            f.seek(0)
            f.write(text)
            f.truncate()

        logging.info("Running initial guess")
        allesfitter.show_initial_guess(allesfit_dir)
        self.custom_plot(candidate_row["name"], candidate_row["period"], fit_width, allesfit_dir, "initial_guess")
        if not self.only_initial:
            logging.info("Preparing bayesian fit")
            if not self.mcmc:
                logging.info("Running dynamic nested sampling")
                allesfitter.ns_fit(allesfit_dir)
                allesfitter.ns_output(allesfit_dir)
            elif self.mcmc:
                logging.info("Running MCMC")
                allesfitter.mcmc_fit(allesfit_dir)
                allesfitter.mcmc_output(allesfit_dir)
            logging.info("Generating custom plots")
            self.custom_plot(candidate_row["name"], candidate_row["period"], fit_width, allesfit_dir, "posterior")

    def custom_plot(self, name, period, fit_width, allesfit_dir, mode="posterior"):
        allesclass = allesfitter.allesclass(allesfit_dir)
        baseline_width = fit_width * 24
        baseline_to_period = fit_width / period
        fig, axes = plt.subplots(2, 3, figsize=(18, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex='col')
        fig.subplots_adjust(left=0.5, right=1.5, hspace=0)
        style = 'full'
        allesclass.plot('lc', name, style, ax=axes[0][0], mode=mode)
        axes[0][0].set_title('lc, ' + style)
        allesclass.plot('lc', name, style + '_residuals', ax=axes[1][0], mode=mode)
        axes[1][0].set_title('')
        style = 'phase'
        allesclass.plot('lc', name, style, ax=axes[0][1], mode=mode, zoomwindow=baseline_to_period)
        axes[0][1].set_title('lc, ' + style)
        axes[0][1].set_xlim([- baseline_to_period / 2, baseline_to_period / 2])
        allesclass.plot('lc', name, style + '_residuals', ax=axes[1][1], mode=mode, zoomwindow=baseline_to_period)
        axes[1][1].set_title('')
        axes[1][1].set_xlim([- baseline_to_period / 2, baseline_to_period / 2])
        style = 'phasezoom'
        allesclass.plot('lc', name, style, ax=axes[0][2], mode=mode, zoomwindow=baseline_width)
        axes[0][2].set_title('lc, ' + style)
        axes[0][2].set_xlim([- baseline_width / 2, baseline_width / 2])
        allesclass.plot('lc', name, style + '_residuals', ax=axes[1][2], mode=mode, zoomwindow=baseline_width)
        axes[1][2].set_title('')
        axes[1][2].set_xlim([- baseline_width / 2, baseline_width / 2])
        fig.savefig(allesfit_dir + '/results/ns_' + mode + '_' + name + '_custom.pdf', bbox_inches='tight')
        style = ['phasezoom_occ']
        style = ['phase_variations']


if __name__ == '__main__':
    ap = ArgumentParser(description='Fitting of Sherlock objects of interest')
    ap.add_argument('--object_dir',
                    help="If the object directory is not your current one you need to provide the ABSOLUTE path",
                    required=False)
    ap.add_argument('--candidate', type=int, default=None, help="The candidate signal to be used.", required=False)
    ap.add_argument('--only_initial', dest='only_initial', action='store_true',
                        help="Whether to only run an initial guess of the transit")
    ap.set_defaults(only_initial=False)
    ap.add_argument('--cpus', type=int, default=None, help="The number of CPU cores to be used.", required=False)
    ap.add_argument('--mcmc', dest='mcmc', action='store_true', help="Whether to run using mcmc or ns. Default is ns.")
    ap.add_argument('--detrend', dest='detrend', default="hybrid_spline", help="Type of detrending to be used", required=False,
                    choices=['no', 'gp'])
    ap.add_argument('--properties', help="The YAML file to be used as input.", required=False)
    args = ap.parse_args()
    fitter = Fitter(args.object_dir, args.only_initial, args.mcmc, args.detrend)
    file_dir = fitter.object_dir + "/fit.log"
    if os.path.exists(file_dir):
        os.remove(file_dir)
    formatter = logging.Formatter('%(message)s')
    logger = logging.getLogger()
    while len(logger.handlers) > 0:
        logger.handlers.pop()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.FileHandler(file_dir)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    index = 0
    fitting_dir = fitter.data_dir + "/fit_" + str(index)
    while os.path.exists(fitting_dir) or os.path.isdir(fitting_dir):
        fitting_dir = fitter.data_dir + "/fit_" + str(index)
        index = index + 1
    os.mkdir(fitting_dir)
    fitter.data_dir = fitter.object_dir
    star_df = pd.read_csv(fitter.data_dir + "/params_star.csv")
    if args.candidate is None:
        user_properties = yaml.load(open(args.properties), yaml.SafeLoader)
        candidate = pd.DataFrame(columns=['id', 'period', 't0', 'cpus', 'rp_rs', 'a', 'number', 'name', 'lc'])
        candidate = candidate.append(user_properties["planet"], ignore_index=True)
        user_star_df = pd.DataFrame(columns=['R_star', 'M_star'])
        if "star" in user_properties and user_properties["star"] is not None:
            user_star_df = user_star_df.append(user_properties["star"], ignore_index=True)
            if user_star_df.iloc[0]["R_star"] is not None:
                star_df.at[0, "R_star"] = user_star_df.iloc[0]["R_star"]
            if user_star_df.iloc[0]["M_star"] is not None:
                star_df.at[0, "M_star"] = user_star_df.iloc[0]["M_star"]
            if user_star_df.iloc[0]["ld_a"] is not None:
                star_df.at[0, "ld_a"] = user_star_df.iloc[0]["ld_a"]
            if user_star_df.iloc[0]["ld_b"] is not None:
                star_df.at[0, "ld_b"] = user_star_df.iloc[0]["ld_b"]
            if ("a" not in user_properties["planet"] or user_properties["planet"]["a"] is None)\
                    and star_df.iloc[0]["M_star"] is not None and not np.isnan(star_df.iloc[0]["M_star"]):
                candidate.at[0, "a"] = HabitabilityCalculator() \
                    .calculate_semi_major_axis(user_properties["planet"]["period"],
                                               user_properties["star"]["M_star"])
            elif ("a" not in user_properties["planet"] or user_properties["planet"]["a"] is None)\
                    and (star_df.iloc[0]["M_star"] is None or np.isnan(star_df.iloc[0]["M_star"])):
                raise ValueError("Cannot guess semi-major axis without star mass.")
        if candidate.iloc[0]["a"] is None or np.isnan(candidate.iloc[0]["a"]):
            raise ValueError("Semi-major axis is neither provided nor inferred.")
        if candidate.iloc[0]["name"] is None:
            raise ValueError("You need to provide a name for your candidate.")
        if candidate.iloc[0]["lc"] is None:
            raise ValueError("You need to provide a light curve relative path for your candidate.")
        cpus = user_properties["settings"]["cpus"]
    else:
        candidate_selection = int(args.candidate)
        candidates = pd.read_csv(fitter.object_dir + "/candidates.csv")
        if candidate_selection < 1 or candidate_selection > len(candidates.index):
            raise SystemExit("User selected a wrong candidate number.")
        candidates = candidates.rename(columns={'Object Id': 'TICID'})
        candidate = candidates.iloc[[candidate_selection - 1]]
        candidate['number'] = [candidate_selection]
        candidate['name'] = 'SOI_' + candidate['number'].astype(str)
        if args.cpus is None:
            cpus = multiprocessing.cpu_count() - 1
        else:
            cpus = args.cpus
        logging.info("Selected signal number " + str(candidate_selection))
    fitter.fit(candidate, star_df, cpus, fitting_dir)
